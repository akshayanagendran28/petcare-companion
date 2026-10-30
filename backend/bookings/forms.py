from datetime import timedelta, datetime
from django import forms
from django.utils import timezone
from .models import Booking
from .utils import validate_caretaker_capacity_for_range
from pets.models import Pet


class BookingCreateForm(forms.ModelForm):
    # Multi-pet checkboxes
    pets = forms.ModelMultipleChoiceField(
        queryset=Pet.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input pet-checkbox'}),
        required=False,
        label="Select Your Pet(s)"
    )

    # Emergency booking fields
    is_emergency = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_emergency'}),
        label="Emergency / Same-Day Booking"
    )
    emergency_phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Urgent phone number (e.g. 9876543210)',
            'id': 'id_emergency_phone'
        }),
        label="Emergency Contact Phone"
    )
    emergency_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Reason for emergency care (e.g., sudden travel, medical emergency, unplanned overtime)...',
            'id': 'id_emergency_reason'
        }),
        label="Reason for Emergency Booking"
    )
    arrival_time = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 02:30 PM (must be at least 1 hr from now)',
            'id': 'id_arrival_time'
        }),
        label="Preferred Arrival Time"
    )
    start_time = forms.CharField(
        required=False,
        max_length=10,
        initial='09:00 AM',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 09:00 AM', 'id': 'id_start_time'})
    )
    end_time = forms.CharField(
        required=False,
        max_length=10,
        initial='05:00 PM',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 05:00 PM', 'id': 'id_end_time'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.caretaker = kwargs.pop('caretaker', None)
        super().__init__(*args, **kwargs)

        today_str = timezone.now().date().strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs.update({
            'min': today_str,
            'class': 'form-control',
            'type': 'date',
            'id': 'id_start_date'
        })
        self.fields['end_date'].widget.attrs.update({
            'min': today_str,
            'class': 'form-control',
            'type': 'date',
            'id': 'id_end_date'
        })

        if user:
            user_pets = Pet.objects.filter(owner=user)
            self.fields['pets'].queryset = user_pets
            self.fields['pet'].queryset = user_pets
            self.fields['pet'].required = False
            self.fields['pet'].widget = forms.HiddenInput()

    class Meta:
        model = Booking
        fields = [
            'pet', 'pets', 'service_type', 'start_date', 'end_date',
            'start_time', 'end_time', 'notes',
            'is_emergency', 'emergency_phone', 'emergency_reason', 'arrival_time'
        ]
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_service_type'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_start_date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_end_date'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 09:00 AM', 'id': 'id_start_time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 05:00 PM', 'id': 'id_end_time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Feeding schedule, emergency vet notes, medicine timings...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_emergency = cleaned_data.get('is_emergency', False)
        selected_pets = cleaned_data.get('pets')
        single_pet = cleaned_data.get('pet')

        # 1. Multi-Pet Validation: Must select at least one pet
        if not selected_pets and not single_pet:
            self.add_error('pets', 'Please choose at least one pet for this booking.')
        elif not selected_pets and single_pet:
            cleaned_data['pets'] = [single_pet]

        if start_date and end_date:
            today = timezone.now().date()
            if start_date < today:
                self.add_error('start_date', 'Start date cannot be in the past.')
            if end_date < start_date:
                self.add_error('end_date', 'End date must be on or after start date.')

            # 2. Advance Booking Rule
            # Standard booking must be booked at least 2 days in advance (start_date >= today + 2 days)
            standard_min_date = today + timedelta(days=2)
            if not is_emergency and start_date < standard_min_date:
                self.add_error(
                    'start_date',
                    f"Standard bookings must be made at least 2 days in advance (earliest available: {standard_min_date.strftime('%B %d, %Y')}). "
                    f"If you need urgent or same-day care, please check the 'Emergency Booking' option below."
                )

            # 3. Emergency Booking Requirements (At least 1 hour notice)
            if is_emergency:
                emergency_phone = cleaned_data.get('emergency_phone', '').strip()
                emergency_reason = cleaned_data.get('emergency_reason', '').strip()
                arrival_time = cleaned_data.get('arrival_time', '').strip()

                if not emergency_phone:
                    self.add_error('emergency_phone', 'Emergency contact phone number is required.')
                if not emergency_reason:
                    self.add_error('emergency_reason', 'Please specify the reason for this emergency care booking.')
                if not arrival_time:
                    self.add_error('arrival_time', 'Please enter preferred arrival time (minimum 1 hour notice required).')

                # If booking for today, check 1 hour advance rule
                if start_date == today:
                    now = timezone.localtime()
                    # Try to parse start_time or arrival_time
                    time_candidate = arrival_time or cleaned_data.get('start_time', '')
                    time_valid = True
                    for fmt in ('%I:%M %p', '%H:%M', '%I:%M%p', '%I %p'):
                        try:
                            parsed_t = datetime.strptime(time_candidate.strip().upper(), fmt).time()
                            requested_dt = timezone.make_aware(datetime.combine(today, parsed_t))
                            if requested_dt < now + timedelta(minutes=50):
                                self.add_error(
                                    'arrival_time',
                                    f"Emergency bookings for today must be scheduled at least 1 hour in advance (current time: {now.strftime('%I:%M %p')})."
                                )
                                time_valid = False
                            break
                        except ValueError:
                            continue

            # 4. Caretaker 1 Booking Per Day Limit
            if self.caretaker and start_date >= today and end_date >= start_date:
                exclude_id = self.instance.pk if (self.instance and self.instance.pk) else None
                is_valid, conflict_date, next_avail = validate_caretaker_capacity_for_range(
                    self.caretaker, start_date, end_date, exclude_booking_id=exclude_id
                )
                if not is_valid:
                    conflict_str = conflict_date.strftime('%B %d, %Y')
                    next_str = next_avail.strftime('%B %d, %Y') if next_avail else 'a later date'
                    err_msg = (
                        f"This caretaker is already booked on {conflict_str} by another pet owner. "
                        f"Caretakers accept strictly 1 booking per day. "
                        f"Please choose another date or select the next open date on {next_str}."
                    )
                    self.add_error('start_date', err_msg)
                    if end_date and conflict_date != start_date:
                        self.add_error('end_date', err_msg)

                # Check if this owner already has an active pending request
                if self.user and self.caretaker:
                    user_pending = Booking.objects.filter(
                        owner=self.user,
                        caretaker=self.caretaker,
                        status='PENDING',
                        start_date__lte=end_date,
                        end_date__gte=start_date
                    )
                    if exclude_id:
                        user_pending = user_pending.exclude(id=exclude_id)
                    if user_pending.exists():
                        self.add_error(
                            'start_date',
                            "You already have a pending booking request with this caretaker for these dates. Please wait for the caretaker's response."
                        )

        return cleaned_data

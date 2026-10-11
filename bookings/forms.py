from django import forms
from django.utils import timezone
from .models import Booking
from .utils import validate_caretaker_capacity_for_range
from pets.models import Pet


class BookingCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.caretaker = kwargs.pop('caretaker', None)
        super().__init__(*args, **kwargs)

        today_str = timezone.now().date().strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs.update({
            'min': today_str,
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['end_date'].widget.attrs.update({
            'min': today_str,
            'class': 'form-control',
            'type': 'date'
        })

        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
            self.fields['pet'].empty_label = "-- Select Your Pet --"
            self.fields['pet'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Booking
        fields = ['pet', 'service_type', 'start_date', 'end_date', 'start_time', 'end_time', 'notes']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 09:00 AM'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 05:00 PM'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Feeding schedule, emergency vet notes, medicine timings...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            today = timezone.now().date()
            if start_date < today:
                self.add_error('start_date', 'Start date cannot be in the past.')
            if end_date < start_date:
                self.add_error('end_date', 'End date must be on or after start date.')

            # Check caretaker daily limit (Max 2 pets per day)
            if self.caretaker and start_date >= today and end_date >= start_date:
                exclude_id = self.instance.pk if (self.instance and self.instance.pk) else None
                is_valid, conflict_date, next_avail = validate_caretaker_capacity_for_range(
                    self.caretaker, start_date, end_date, exclude_booking_id=exclude_id
                )
                if not is_valid:
                    conflict_str = conflict_date.strftime('%B %d, %Y')
                    next_str = next_avail.strftime('%B %d, %Y') if next_avail else 'a later date'
                    self.add_error(
                        'start_date',
                        f"This caretaker is fully booked on {conflict_str} (maximum daily limit of 2 pets reached). "
                        f"Please choose another date or book for the next available slot on {next_str}."
                    )

        return cleaned_data

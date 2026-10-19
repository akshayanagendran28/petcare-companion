from django import forms
from .models import LostPetReport, LostPetSighting

class LostPetReportForm(forms.ModelForm):
    class Meta:
        model = LostPetReport
        fields = [
            'pet_name', 'species', 'breed', 'gender', 'approx_age', 'color_pattern',
            'distinctive_marks', 'collar_description', 'microchip_id',
            'last_seen_location', 'date_lost', 'time_lost', 'how_lost', 'description',
            'police_complaint_status', 'police_station_name', 'police_csr_number', 'police_filing_date', 'police_contact_details', 'police_document',
            'reward_amount', 'reward_details',
            'contact_name', 'contact_number', 'alternate_contact',
            'photo', 'status', 'reunited_date', 'reunited_details'
        ]
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bruno / Bella / Rocky'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dog, Cat, Bird'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Golden Retriever / Indie / Persian Cat'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'approx_age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2.5 years / 8 months puppy'}),
            'color_pattern': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Honey Golden coat with white chest'}),
            
            # Distinctive marks & identifiers
            'distinctive_marks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. Birth marks: Distinct heart-shaped black patch on inner left leg, white streak on chest, black spot on tongue, docked tail, notched ear...'
            }),
            'collar_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Red reflective nylon collar with metal bell & brass tag "BRUNO"'
            }),
            'microchip_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 981098102345678 or RFID Tag #'
            }),

            # Where, When, How lost
            'last_seen_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Besant Nagar Beach Promenade near 5th Avenue, Chennai'
            }),
            'date_lost': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_lost': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 06:30 PM (Evening Walk) / Early Morning'
            }),
            'how_lost': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. Slipped harness during evening walk after getting startled by sudden festival fireworks; ran towards 4th main road...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g. Very friendly, responds to whistling and the name "Bruno", loves chicken treats, may be scared of moving cars...'
            }),

            # Police complaint details
            'police_complaint_status': forms.Select(attrs={'class': 'form-select', 'id': 'id_police_complaint_status'}),
            'police_station_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. J-3 Guindy Police Station / J-2 Adyar Station, Chennai'
            }),
            'police_csr_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CSR No. 442/2026 or FIR No. 109/2026'
            }),
            'police_filing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'police_contact_details': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Sub-Inspector Ramanathan (044-2345-XXXX)'
            }),
            'police_document': forms.FileInput(attrs={'class': 'form-control'}),

            # Reward
            'reward_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '100', 'placeholder': '0.00'}),
            'reward_details': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ₹10,000 Cash Reward - Instant handover upon safe return, no questions asked'
            }),

            # Contacts
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner / Rescuer Name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'alternate_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 91234 56789 (Alternate/Family)'}),

            # Status & Reunion details
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reunited_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reunited_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g. Safely found on Oct 5 near beach park after a kind neighbor called our helpline. Reunited with family!'
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LostPetSightingForm(forms.ModelForm):
    class Meta:
        model = LostPetSighting
        fields = ['reporter_name', 'reporter_contact', 'sighting_location', 'sighting_date', 'sighting_time', 'description', 'photo']
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'reporter_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number or Email'}),
            'sighting_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exact Street, Landmark, Shop name, or Crossroad'}),
            'sighting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sighting_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 07:30 AM / 2 hours ago'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what you saw: direction the pet was walking, collar/marks observed, pet health condition, who was nearby...'
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import MatchProfile, MatchRequest
from pets.models import Pet

class MatchProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not self.instance.pk:
            # Only show pets that do NOT already have a match profile
            existing_pet_ids = MatchProfile.objects.values_list('pet_id', flat=True)
            self.fields['pet'].queryset = Pet.objects.filter(owner=user).exclude(id__in=existing_pet_ids)
            self.fields['pet'].empty_label = "-- Select Your Pet --"
            self.fields['pet'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = MatchProfile
        fields = ['pet', 'looking_for', 'location', 'bio', 'is_active']
        widgets = {
            'looking_for': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Neighborhood / City'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Personality, energy level, friendliness with other dogs/cats...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MatchRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        receiver = kwargs.pop('receiver_profile', None)
        super().__init__(*args, **kwargs)
        if user:
            user_profiles = MatchProfile.objects.filter(pet__owner=user, is_active=True)
            if receiver:
                user_profiles = user_profiles.exclude(pk=receiver.pk)
            self.fields['sender_profile'].queryset = user_profiles
            self.fields['sender_profile'].label = "Select Your Pet's Match Profile"
            self.fields['sender_profile'].empty_label = "-- Choose Profile --"
            self.fields['sender_profile'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = MatchRequest
        fields = ['sender_profile', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Hi! Would love to meet up at the park for a playdate...'
            }),
        }

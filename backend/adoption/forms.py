from django import forms
from .models import AdoptionListing

class AdoptionListingForm(forms.ModelForm):
    class Meta:
        model = AdoptionListing
        fields = [
            'pet_name', 'species', 'breed', 'age', 'gender',
            'listing_type', 'price', 'location', 'vaccination_status',
            'description', 'photo', 'contact_phone', 'contact_email'
        ]
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dog / Cat / Other'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Golden Retriever'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Age in years'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'vaccination_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Up to date, Dewormed'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Personality, energy level, friendliness with children...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@email.com'}),
        }

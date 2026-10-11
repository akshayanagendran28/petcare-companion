from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'species', 'breed', 'age', 'gender', 'weight',
            'health_condition', 'activity_level', 'vaccination_status',
            'allergies', 'medical_notes', 'photo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Buddy'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dog / Cat'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Golden Retriever'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Years'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'kg'}),
            'health_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Healthy / Any condition'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'vaccination_status': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chicken, Pollen (or None)'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Emergency instructions, vet info, dietary notes...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

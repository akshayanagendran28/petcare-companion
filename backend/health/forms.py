from django import forms
from .models import HealthRecord, VaccinationRecord, MedicineRecord, WeightRecord, AllergyRecord

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['record_date', 'condition_title', 'diagnosis', 'treatment_plan', 'vet_name', 'clinic_name']
        widgets = {
            'record_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'condition_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Annual Checkup / Ear Infection'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Vet findings...'}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Prescriptions, rest advice, follow up...'}),
            'vet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Smith'}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Animal Hospital'}),
        }


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['vaccine_name', 'administered_date', 'next_due_date', 'batch_number', 'vet_name']
        widgets = {
            'vaccine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rabies 3-Year Booster'}),
            'administered_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch / Lot # (optional)'}),
            'vet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Administered by Dr. ...'}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = MedicineRecord
        fields = ['medicine_name', 'dosage', 'frequency', 'start_date', 'end_date', 'notes', 'is_active']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Amoxicillin'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 250mg capsule'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Twice daily after food'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Special notes...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['recorded_date', 'weight_kg', 'notes']
        widgets = {
            'recorded_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'kg'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Post-exercise / Regular check'}),
        }


class AllergyForm(forms.ModelForm):
    class Meta:
        model = AllergyRecord
        fields = ['allergy_name', 'severity', 'notes']
        widgets = {
            'allergy_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Beef Protein, Grass Pollen'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Reactions and antihistamine response...'}),
        }

from django.db import models
from django.utils import timezone
from datetime import timedelta
from pets.models import Pet

class HealthRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='health_records')
    record_date = models.DateField(default=timezone.now)
    condition_title = models.CharField(max_length=200, help_text='e.g. Annual Checkup, Ear Infection, Dental Cleaning')
    diagnosis = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    vet_name = models.CharField(max_length=150, blank=True, null=True)
    clinic_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'HEALTH_RECORDS'
        verbose_name = 'Health Record'
        verbose_name_plural = 'Health Records'
        ordering = ['-record_date']

    def __str__(self):
        return f"{self.condition_title} - {self.pet.name} ({self.record_date})"


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=150, help_text='e.g. Rabies, DHPP, Bordetella, FVRCP')
    administered_date = models.DateField()
    next_due_date = models.DateField(help_text='Next booster shot due date')
    batch_number = models.CharField(max_length=50, blank=True, null=True)
    vet_name = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'VACCINATIONS'
        verbose_name = 'Vaccination Record'
        verbose_name_plural = 'Vaccination Records'
        ordering = ['-administered_date']

    def __str__(self):
        return f"{self.vaccine_name} - {self.pet.name} (Due: {self.next_due_date})"

    @property
    def reminder_status(self):
        today = timezone.now().date()
        if self.next_due_date < today:
            return 'OVERDUE'
        elif self.next_due_date <= today + timedelta(days=7):
            return 'DUE_SOON'
        return 'UPCOMING'

    @property
    def days_remaining(self):
        today = timezone.now().date()
        return (self.next_due_date - today).days


class MedicineRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100, help_text='e.g. 1 Tablet (20mg), 5ml')
    frequency = models.CharField(max_length=100, help_text='e.g. Twice daily with meals, Once every 12 hours')
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True, help_text='Side effects, administration tips...')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MEDICINES'
        verbose_name = 'Medicine Record'
        verbose_name_plural = 'Medicine Records'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage}) for {self.pet.name}"


class WeightRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='weight_history')
    recorded_date = models.DateField(default=timezone.now)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'WEIGHT_HISTORY'
        verbose_name = 'Weight History Record'
        verbose_name_plural = 'Weight History Records'
        ordering = ['recorded_date']

    def __str__(self):
        return f"{self.pet.name}: {self.weight_kg} kg on {self.recorded_date}"


class AllergyRecord(models.Model):
    SEVERITY_CHOICES = (
        ('Mild', 'Mild (Itching / Skin dry)'),
        ('Moderate', 'Moderate (Digestive upset / Rash)'),
        ('Severe', 'Severe (Anaphylaxis / Breathing issue)'),
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='allergy_records')
    allergy_name = models.CharField(max_length=150, help_text='e.g. Chicken, Beef, Flea Saliva, Penicillin')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Moderate')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ALLERGIES'
        verbose_name = 'Allergy Record'
        verbose_name_plural = 'Allergy Records'

    def __str__(self):
        return f"{self.allergy_name} ({self.severity}) - {self.pet.name}"

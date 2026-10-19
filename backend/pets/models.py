from django.db import models
from django.conf import settings
from django.urls import reverse
import os
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Pet(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    ACTIVITY_CHOICES = (
        ('Low', 'Low (Calm / Indoor)'),
        ('Moderate', 'Moderate (1-2 walks/day)'),
        ('High', 'High (Energetic / Active)'),
        ('Very High', 'Very High (Agility / Athletic)'),
    )

    VACCINE_CHOICES = (
        ('Up to Date', 'Up to Date'),
        ('Due Soon', 'Due Soon'),
        ('Overdue', 'Overdue'),
        ('Not Vaccinated', 'Not Vaccinated'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=30, default='Dog')
    breed = models.CharField(max_length=100)
    age = models.DecimalField(max_digits=4, decimal_places=1, help_text='Age in years (e.g. 2.5)')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight in kg')
    health_condition = models.CharField(max_length=100, default='Healthy')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='Moderate')
    vaccination_status = models.CharField(max_length=20, choices=VACCINE_CHOICES, default='Up to Date')
    allergies = models.CharField(max_length=255, blank=True, null=True, help_text='Known food/environmental allergies')
    medical_notes = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='pets/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PETS'
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.breed})"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default_pet.svg'

    def get_qr_url(self):
        if self.qr_code and hasattr(self.qr_code, 'url'):
            return self.qr_code.url
        return ''

    def get_emergency_url(self):
        return reverse('pets:emergency_profile', kwargs={'pk': self.pk})

    def generate_qr_code(self, host_domain="http://127.0.0.1:8000"):
        """Generates QR code linking to the pet's emergency profile."""
        emergency_url = f"{host_domain}{self.get_emergency_url()}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3,
        )
        qr.add_data(emergency_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1e293b", back_color="#ffffff")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"qr_pet_{self.pk}_{self.name.lower()}.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])

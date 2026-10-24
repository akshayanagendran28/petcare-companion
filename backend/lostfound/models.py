from django.db import models
from django.conf import settings
from django.utils import timezone

class LostPetReport(models.Model):
    STATUS_CHOICES = (
        ('LOST', 'Currently Lost / Missing 🔍'),
        ('FOUND', 'Found by Rescuer / Safe Shelter 🏠'),
        ('REUNITED', 'Safely Reunited! 🎉'),
        ('SIGHTING_REPORTED', 'Recent Verified Sighting 👁️'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown / Not Specified'),
    )

    POLICE_STATUS_CHOICES = (
        ('FILED', 'Official Police Complaint / CSR Filed ✅'),
        ('UNDER_REVIEW', 'Complaint Submitted (Pending CSR) ⏳'),
        ('NOT_FILED', 'Not Filed / Private Community Search 📋'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_pet_reports')
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=30, default='Dog')
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='Male')
    approx_age = models.CharField(max_length=50, blank=True, null=True, help_text='e.g. 2.5 years, 8 months puppy')
    color_pattern = models.CharField(max_length=150, blank=True, null=True, help_text='e.g. Golden brown, Tri-color black & white, Tabby stripes')
    
    # Detailed birthmarks & identification
    distinctive_marks = models.TextField(
        blank=True, null=True,
        help_text='Distinct birth marks, coat patches, eye colors, docked tail, notched ears, unique scars...'
    )
    collar_description = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='e.g. Red reflective collar with silver bell & tag'
    )
    microchip_id = models.CharField(max_length=100, blank=True, null=True, help_text='Microchip ID / Tag Number')

    # Where, When & How lost
    last_seen_location = models.CharField(max_length=255, help_text='Street, Area, Landmark, City (e.g. Besant Nagar Beach Promenade, Chennai)')
    date_lost = models.DateField(default=timezone.now)
    time_lost = models.CharField(max_length=100, blank=True, null=True, help_text='e.g. 06:30 PM (Evening Walk), Dawn, Midday')
    how_lost = models.TextField(
        blank=True, null=True,
        help_text='Detailed circumstances: how the pet went missing, slipped harness, scared by thunder/fireworks, escaped gate...'
    )
    description = models.TextField(
        blank=True, null=True,
        help_text='General personality, behavioral cues (friendly, skittish, responds to treat names)...'
    )

    # Police Complaint & Official Record details
    police_complaint_status = models.CharField(
        max_length=30, choices=POLICE_STATUS_CHOICES, default='NOT_FILED'
    )
    police_station_name = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='e.g. J-3 Guindy Police Station / E-5 Foreshore Estate Station, Chennai'
    )
    police_csr_number = models.CharField(
        max_length=100, blank=True, null=True,
        help_text='e.g. CSR No. 442/2026 or FIR No. 108/2026'
    )
    police_filing_date = models.DateField(blank=True, null=True, help_text='Date when police complaint was recorded')
    police_contact_details = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='Station contact or Investigating Officer details'
    )
    police_document = models.FileField(
        upload_to='police_docs/', blank=True, null=True,
        help_text='Uploaded official Police CSR copy / acknowledgement slip (Image or PDF)'
    )
    police_verified_by_ai = models.BooleanField(
        default=False,
        help_text='Whether this police report was authenticated by the ML Document Inspector'
    )
    police_verification_confidence = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        help_text='ML Verification Confidence Score (%)'
    )
    police_verification_details = models.TextField(
        blank=True, null=True,
        help_text='ML extracted features, official seal detection, and audit breakdown'
    )
    police_verified_at = models.DateTimeField(
        blank=True, null=True,
        help_text='Timestamp when ML verification was performed'
    )

    # Reward details
    reward_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,
        help_text='Reward amount in ₹ (₹0 if none)'
    )
    reward_details = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='e.g. ₹10,000 Cash Reward - Guaranteed on safe return, no questions asked'
    )

    # Contact & Recovery Details
    contact_name = models.CharField(max_length=150, blank=True, null=True, help_text='Primary Contact / Owner Name')
    contact_number = models.CharField(max_length=30, help_text='Primary Phone Number')
    alternate_contact = models.CharField(max_length=50, blank=True, null=True, help_text='Emergency Alternate Phone')
    
    photo = models.ImageField(upload_to='lost_pets/', blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='LOST')

    # Already lost / reunited resolution details
    reunited_date = models.DateField(blank=True, null=True, help_text='Date of successful reunion')
    reunited_details = models.TextField(
        blank=True, null=True,
        help_text='Story / Resolution details: how the pet was found, who helped, location of recovery...'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'LOST_PETS'
        verbose_name = 'Lost Pet Report'
        verbose_name_plural = 'Lost Pet Reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.status}: {self.pet_name} ({self.breed}) at {self.last_seen_location}"

    @property
    def has_police_complaint(self):
        """Returns True if an official police complaint / CSR has been registered."""
        if self.police_complaint_status == 'FILED' or self.police_verified_by_ai:
            return True
        if self.police_csr_number and self.police_csr_number.strip():
            return True
        if self.police_station_name and self.police_station_name.strip() and self.police_complaint_status != 'NOT_FILED':
            return True
        return False

    def save(self, *args, **kwargs):
        # Auto-update status to FILED if CSR number or station is provided
        if (self.police_csr_number or self.police_station_name or self.police_document) and self.police_complaint_status == 'NOT_FILED':
            self.police_complaint_status = 'FILED'
        super().save(*args, **kwargs)

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default_pet.svg'


class LostPetSighting(models.Model):
    lost_pet = models.ForeignKey(LostPetReport, on_delete=models.CASCADE, related_name='sightings')
    reporter_name = models.CharField(max_length=150, help_text='Your Name')
    reporter_contact = models.CharField(max_length=100, help_text='Phone number or Email')
    sighting_location = models.CharField(max_length=255, help_text='Where did you spot the pet? (Street, Landmark, City)')
    sighting_date = models.DateField(default=timezone.now)
    sighting_time = models.CharField(max_length=50, blank=True, null=True, help_text='e.g. 07:15 AM, Afternoon')
    description = models.TextField(help_text='Direction heading, pet condition, collar seen, surroundings...')
    photo = models.ImageField(upload_to='sightings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'LOST_PET_SIGHTINGS'
        verbose_name = 'Lost Pet Sighting'
        verbose_name_plural = 'Lost Pet Sightings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Sighting of {self.lost_pet.pet_name} at {self.sighting_location}"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return None

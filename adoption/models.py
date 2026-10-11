from django.db import models
from django.conf import settings

class AdoptionListing(models.Model):
    TYPE_CHOICES = (
        ('ADOPTION', 'Adoption (Free / Rehoming)'),
        ('SALE', 'Pet Sale / Breeder'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active Listing'),
        ('PENDING', 'Adoption Pending'),
        ('ADOPTED', 'Adopted / Found Home'),
        ('SOLD', 'Sold'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_listings')
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=30, default='Dog')
    breed = models.CharField(max_length=100)
    age = models.DecimalField(max_digits=4, decimal_places=1, help_text='Age in years')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    listing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ADOPTION')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Adoption fee or sale price ($0 for free)')
    location = models.CharField(max_length=200, help_text='City, State')
    vaccination_status = models.CharField(max_length=50, default='Fully Vaccinated')
    description = models.TextField(help_text='Personality, habits, reason for rehoming, compatibility with children/other pets...')
    photo = models.ImageField(upload_to='listings/', blank=True, null=True)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ADOPTION_LISTINGS'
        verbose_name = 'Adoption Listing'
        verbose_name_plural = 'Adoption Listings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet_name} - {self.breed} ({self.listing_type})"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default_pet.svg'

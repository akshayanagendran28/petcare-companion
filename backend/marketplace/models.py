from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class CaretakerProfile(models.Model):
    AVAILABILITY_CHOICES = (
        ('AVAILABLE', 'Available Now'),
        ('BUSY', 'Busy / Limited Slots'),
        ('UNAVAILABLE', 'Unavailable'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='caretaker_profile')
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=25.00)
    services_offered = models.CharField(max_length=500, default='Pet Sitting, Dog Walking, Daycare')
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='AVAILABLE')
    bio = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_reviews = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'CARETAKERS'
        verbose_name = 'Caretaker Profile'
        verbose_name_plural = 'Caretaker Profiles'
        ordering = ['-rating', '-total_reviews']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.experience_years} yrs exp)"

    def clean(self):
        super().clean()
        if self.hourly_rate is not None and self.hourly_rate <= 0:
            raise ValidationError({'hourly_rate': 'Hourly rate must be a positive number greater than zero (minimum ₹50/hr).'})
        if self.experience_years is not None and self.experience_years < 0:
            raise ValidationError({'experience_years': 'Experience years cannot be negative.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_services_list(self):
        return [s.strip() for s in self.services_offered.split(',') if s.strip()]

    def update_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(caretaker=self)
        if reviews.exists():
            avg = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 5.0
            self.rating = round(avg, 2)
            self.total_reviews = reviews.count()
            self.save(update_fields=['rating', 'total_reviews'])

    def get_recommended_hourly_rate(self):
        """
        Calculates an intelligent recommended hourly salary / rate quote (₹/hr)
        based on verified experience years and customer feedback rating & reviews.
        Formula:
          Base Rate: ₹150/hr
          Experience Bonus: ₹40 per year of experience (max ₹400 for 10+ yrs)
          Feedback Rating Bonus:
            - 4.8★ - 5.0★: +₹150
            - 4.4★ - 4.7★: +₹100
            - 4.0★ - 4.3★: +₹50
            - Below 4.0★: +₹0
          Review Volume Bonus: +₹5 per review (max ₹100 for 20+ reviews)
          Round to nearest ₹10.
        """
        exp = float(self.experience_years or 0)
        rating_val = float(self.rating or 5.0)
        reviews_val = int(self.total_reviews or 0)

        base_rate = 150.0
        exp_bonus = min(max(0.0, exp) * 40.0, 400.0)

        if rating_val >= 4.8:
            rating_bonus = 150.0
        elif rating_val >= 4.4:
            rating_bonus = 100.0
        elif rating_val >= 4.0:
            rating_bonus = 50.0
        else:
            rating_bonus = 0.0

        reviews_bonus = min(reviews_val * 5.0, 100.0)

        rec = base_rate + exp_bonus + rating_bonus + reviews_bonus
        # Round to nearest ₹10
        recommended = round(rec / 10.0) * 10.0
        return Decimal(str(max(150.0, recommended)))

    def get_recommended_rate_range(self):
        """Returns tuple (recommended_min, recommended_max, recommended_optimal)"""
        optimal = float(self.get_recommended_hourly_rate())
        min_rate = round((optimal * 0.85) / 10.0) * 10.0
        max_rate = round((optimal * 1.25) / 10.0) * 10.0
        return (Decimal(str(min_rate)), Decimal(str(max_rate)), Decimal(str(optimal)))

    @property
    def capacity_summary(self):
        from bookings.utils import get_caretaker_capacity_summary
        return get_caretaker_capacity_summary(self)

    @property
    def is_fully_booked_today(self):
        return self.capacity_summary['is_fully_booked']



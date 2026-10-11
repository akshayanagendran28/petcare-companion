from django.db import models
from django.conf import settings

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

    @property
    def capacity_summary(self):
        from bookings.utils import get_caretaker_capacity_summary
        return get_caretaker_capacity_summary(self)

    @property
    def is_fully_booked_today(self):
        return self.capacity_summary['is_fully_booked']


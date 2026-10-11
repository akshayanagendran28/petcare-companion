from django.db import models
from django.conf import settings
from pets.models import Pet
from marketplace.models import CaretakerProfile

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Confirmation'),
        ('ACCEPTED', 'Accepted / Upcoming'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    SERVICE_CHOICES = (
        ('Pet Sitting', 'Pet Sitting (In-Home)'),
        ('Dog Walking', 'Dog Walking & Exercise'),
        ('Overnight Boarding', 'Overnight Boarding'),
        ('Daycare', 'Daycare & Socialization'),
        ('Grooming & Bath', 'Grooming & Bathing'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    caretaker = models.ForeignKey(CaretakerProfile, on_delete=models.CASCADE, related_name='bookings')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES, default='Pet Sitting')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.CharField(max_length=10, default='09:00 AM')
    end_time = models.CharField(max_length=10, default='05:00 PM')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True, help_text='Diet instructions, walking routine, special habits...')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BOOKINGS'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.pet.name} with {self.caretaker.user.get_full_name() or self.caretaker.user.username} ({self.status})"

    @property
    def duration_days(self):
        delta = (self.end_date - self.start_date).days
        return max(1, delta + 1)

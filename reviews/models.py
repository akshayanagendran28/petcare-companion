from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from bookings.models import Booking
from marketplace.models import CaretakerProfile

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    caretaker = models.ForeignKey(CaretakerProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 (poor) to 5 (excellent)'
    )
    comment = models.TextField(help_text='Share your experience with this caretaker...')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'REVIEWS'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ by {self.reviewer.username} for {self.caretaker.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.caretaker.update_rating()

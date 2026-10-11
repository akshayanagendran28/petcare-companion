from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = (
        ('BOOKING', 'Booking Update'),
        ('REMINDER', 'Vaccine / Health Reminder'),
        ('MATCH', 'Pet Match Alert'),
        ('LOST_FOUND', 'Lost & Found Sighting'),
        ('REVIEW', 'New Review'),
        ('GENERAL', 'General Notification'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=500)
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='GENERAL')
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'NOTIFICATIONS'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user.username} ({'Read' if self.is_read else 'Unread'})"

from django.db import models
from django.conf import settings

class BreedScanLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='breed_scans')
    image = models.ImageField(upload_to='scans/')
    predicted_breed = models.CharField(max_length=100)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BREED_SCANS'
        verbose_name = 'Breed Scan Log'
        verbose_name_plural = 'Breed Scan Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.predicted_breed} ({self.confidence_score}%) on {self.created_at.strftime('%Y-%m-%d')}"

from django.db import models
from django.conf import settings
from pets.models import Pet

class RecommendationLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, blank=True, null=True, related_name='recommendation_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    input_breed = models.CharField(max_length=100)
    input_age = models.DecimalField(max_digits=4, decimal_places=1)
    input_weight = models.DecimalField(max_digits=5, decimal_places=2)
    input_health = models.CharField(max_length=100)
    input_activity = models.CharField(max_length=50)
    diet_category = models.CharField(max_length=150)
    recommended_food = models.CharField(max_length=200)
    recommended_service = models.CharField(max_length=200)
    care_tip = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'RECOMMENDATIONS'
        verbose_name = 'Recommendation Log'
        verbose_name_plural = 'Recommendation Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"Recommendation for {self.input_breed} ({self.created_at.strftime('%Y-%m-%d')})"

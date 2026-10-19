from django.db import models
from pets.models import Pet

class MatchProfile(models.Model):
    LOOKING_FOR_CHOICES = (
        ('Playmate & Walking Buddy', 'Playmate & Walking Buddy'),
        ('Socialization Partner', 'Socialization & Pack Play'),
        ('Breeding Companion', 'Breeding Companion (Pedigree)'),
        ('Agility / Training Partner', 'Agility / Training Partner'),
    )

    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='match_profile')
    bio = models.TextField(help_text='Describe pet temperament, play style, favorite park activities...')
    looking_for = models.CharField(max_length=100, choices=LOOKING_FOR_CHOICES, default='Playmate & Walking Buddy')
    location = models.CharField(max_length=200, help_text='Neighborhood, City')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MATCH_PROFILES'
        verbose_name = 'Match Profile'
        verbose_name_plural = 'Match Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Match Profile for {self.pet.name} ({self.pet.breed})"


class MatchRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Request'),
        ('ACCEPTED', 'Accepted / Matched!'),
        ('REJECTED', 'Declined'),
    )

    sender_profile = models.ForeignKey(MatchProfile, on_delete=models.CASCADE, related_name='sent_requests')
    receiver_profile = models.ForeignKey(MatchProfile, on_delete=models.CASCADE, related_name='received_requests')
    message = models.CharField(max_length=500, blank=True, null=True, help_text='Friendly note to the other pet parent...')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'MATCH_REQUESTS'
        verbose_name = 'Match Request'
        verbose_name_plural = 'Match Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"Match: {self.sender_profile.pet.name} -> {self.receiver_profile.pet.name} ({self.status})"

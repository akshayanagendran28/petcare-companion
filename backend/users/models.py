from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PET_OWNER', 'Pet Owner'),
        ('CARETAKER', 'Caretaker'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PET_OWNER')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    class Meta:
        db_table = 'USERS'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_pet_owner(self):
        return self.role == 'PET_OWNER'

    @property
    def is_caretaker_user(self):
        return self.role == 'CARETAKER'

    def get_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        return '/static/images/default_avatar.svg'

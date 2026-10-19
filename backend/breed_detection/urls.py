from django.urls import path
from . import views

app_name = 'breed_detection'

urlpatterns = [
    path('', views.detect_breed, name='detect_breed'),
]

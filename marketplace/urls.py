from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.caretaker_list, name='caretaker_list'),
    path('<int:pk>/', views.caretaker_detail, name='caretaker_detail'),
]

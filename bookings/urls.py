from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:caretaker_id>/', views.create_booking, name='create_booking'),
    path('api/availability/<int:caretaker_id>/', views.caretaker_availability_api, name='availability_api'),
    path('my-bookings/', views.owner_booking_list, name='owner_list'),
    path('caretaker/requests/', views.caretaker_booking_requests, name='caretaker_requests'),
    path('<int:pk>/<str:action>/', views.update_booking_status, name='update_status'),

]

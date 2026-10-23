from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:caretaker_id>/', views.create_booking, name='create_booking'),
    path('api/availability/<int:caretaker_id>/', views.caretaker_availability_api, name='availability_api'),
    path('my-bookings/', views.owner_booking_list, name='owner_list'),
    path('caretaker/requests/', views.caretaker_booking_requests, name='caretaker_requests'),
    path('<int:booking_id>/payment/', views.booking_payment_view, name='booking_payment'),
    path('<int:booking_id>/receipt/', views.booking_receipt_view, name='booking_receipt'),
    path('<int:booking_id>/payment/checkout/', views.booking_payment_view, name='payment'),
    path('<int:booking_id>/payment/verify/', views.verify_payment_api, name='verify_payment'),
    path('<int:booking_id>/payment/status/', views.check_payment_status_api, name='payment_status'),
    path('<int:booking_id>/payment/failed/', views.payment_failed_api, name='payment_failed'),
    path('<int:pk>/<str:action>/', views.update_booking_status, name='update_status'),
]


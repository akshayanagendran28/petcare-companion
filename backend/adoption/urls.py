from django.urls import path
from . import views

app_name = 'adoption'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('add/', views.listing_create, name='listing_create'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('<int:pk>/payment/', views.adoption_payment_view, name='payment'),
    path('<int:pk>/payment/verify/', views.verify_adoption_payment_api, name='verify_payment'),
    path('<int:pk>/payment/status/', views.check_adoption_payment_status_api, name='payment_status'),
    path('<int:pk>/payment/failed/', views.adoption_payment_failed_api, name='payment_failed'),
    path('<int:pk>/inquire/', views.submit_adoption_inquiry, name='submit_inquiry'),
    path('requests/<int:request_id>/<str:action>/', views.handle_adoption_request, name='handle_request'),
    path('<int:pk>/status/<str:new_status>/', views.listing_update_status, name='update_status'),
]

from django.urls import path
from . import views

app_name = 'adoption'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('add/', views.listing_create, name='listing_create'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('<int:pk>/status/<str:new_status>/', views.listing_update_status, name='update_status'),
]

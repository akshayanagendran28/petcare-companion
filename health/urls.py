from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('reminders/', views.reminders_view, name='reminders'),
    path('<int:pet_id>/', views.health_dashboard, name='dashboard'),
    path('<int:pet_id>/add/<str:record_type>/', views.add_health_record, name='add_record'),
    path('<int:pet_id>/weight-data/', views.weight_data_api, name='weight_data'),
    path('<int:pet_id>/add-weight-ajax/', views.add_weight_ajax, name='add_weight_ajax'),
]

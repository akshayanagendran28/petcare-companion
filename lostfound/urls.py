from django.urls import path
from . import views

app_name = 'lostfound'

urlpatterns = [
    path('', views.lost_pet_list, name='lost_list'),
    path('report/', views.report_lost_pet, name='report_lost'),
    path('<int:pk>/', views.lost_pet_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_lost_pet, name='edit_report'),
    path('<int:pk>/sighting/', views.submit_sighting, name='submit_sighting'),
    path('<int:pk>/reunited/', views.mark_reunited, name='mark_reunited'),
    path('<int:pk>/verify-police-doc/', views.verify_police_document_ajax, name='verify_police_doc'),
]

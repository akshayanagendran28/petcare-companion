from django.urls import path
from . import views

app_name = 'matchhub'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('add-profile/', views.create_profile, name='create_profile'),
    path('request/<int:receiver_id>/', views.send_match_request, name='send_request'),
    path('requests/', views.match_requests_inbox, name='match_requests'),
    path('requests/<int:pk>/<str:action>/', views.update_match_request_status, name='update_status'),
]

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_router, name='dashboard'),
    path('dashboard/owner/', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('dashboard/caretaker/', views.caretaker_dashboard, name='caretaker_dashboard'),
    path('profile/', views.profile_view, name='profile'),
]

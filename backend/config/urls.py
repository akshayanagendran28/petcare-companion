"""Pet Care Companion URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import home_view
from config.health import health_check_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('api/health-check/', health_check_view, name='api_health_check'),
    path('health-check/', health_check_view, name='health_check'),
    path('users/', include('users.urls', namespace='users')),
    path('pets/', include('pets.urls', namespace='pets')),
    path('marketplace/', include('marketplace.urls', namespace='marketplace')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('adoption/', include('adoption.urls', namespace='adoption')),
    path('matchhub/', include('matchhub.urls', namespace='matchhub')),
    path('health/', include('health.urls', namespace='health')),
    path('lostfound/', include('lostfound.urls', namespace='lostfound')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),
    path('recommendations/', include('recommendations.urls', namespace='recommendations')),
    path('breed-detection/', include('breed_detection.urls', namespace='breed_detection')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

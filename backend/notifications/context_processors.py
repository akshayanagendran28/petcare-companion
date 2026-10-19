from .models import Notification

def notification_badge(request):
    """Context processor that exposes unread notification count to all base templates."""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        return {
            'unread_notifications_count': unread_count,
            'navbar_notifications': recent_notifs,
        }
    return {
        'unread_notifications_count': 0,
        'navbar_notifications': [],
    }

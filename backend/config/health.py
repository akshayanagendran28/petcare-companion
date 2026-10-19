"""
Pet Care Companion Health Check Endpoint
Used by Render Web Service monitoring and Vercel Frontend connectivity verification.
"""
from django.http import JsonResponse
from django.db import connection
from django.utils import timezone


def health_check_view(request):
    """
    Returns service health status, active database engine, and connection state.
    """
    db_status = "unknown"
    db_engine = connection.settings_dict.get('ENGINE', 'unknown').split('.')[-1]
    
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    is_healthy = db_status == "connected"

    return JsonResponse({
        "status": "healthy" if is_healthy else "degraded",
        "service": "Pet Care Companion Backend",
        "database": {
            "status": db_status,
            "engine": db_engine,
        },
        "timestamp": timezone.now().isoformat(),
        "cors_enabled": True,
        "hosting": "Render",
    }, status=200 if is_healthy else 503)

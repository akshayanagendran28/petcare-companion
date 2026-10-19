"""
Pet Care Companion Health Check Endpoint
Monitors Render Web Service, Relational Database (PostgreSQL/SQLite), and MongoDB Atlas NoSQL.
"""
from django.http import JsonResponse
from django.db import connection
from django.utils import timezone


def health_check_view(request):
    """
    Returns service health status, active database engine, and MongoDB status.
    """
    db_status = "unknown"
    db_engine = connection.settings_dict.get('ENGINE', 'unknown').split('.')[-1]
    
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check MongoDB status
    mongo_status = {"status": "not_configured"}
    try:
        from config.mongodb import check_mongo_connection
        mongo_status = check_mongo_connection()
    except Exception:
        try:
            from backend.config.mongodb import check_mongo_connection
            mongo_status = check_mongo_connection()
        except Exception as me:
            mongo_status = {"status": "error", "error": str(me)}

    is_healthy = db_status == "connected"

    return JsonResponse({
        "status": "healthy" if is_healthy else "degraded",
        "service": "Pet Care Companion Backend",
        "primary_database": {
            "status": db_status,
            "engine": db_engine,
        },
        "mongodb": mongo_status,
        "timestamp": timezone.now().isoformat(),
        "cors_enabled": True,
        "hosting": "Render",
    }, status=200 if is_healthy else 503)

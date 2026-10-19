"""
Real-time MongoDB Sync Signals
Listens to post_save and post_delete events across all application models
and automatically writes changes to MongoDB Atlas in real time.
"""

from django.db.models.signals import post_save, post_delete
from django.apps import apps
import logging

logger = logging.getLogger('mongodb')

APP_LABELS = {
    'users', 'pets', 'marketplace', 'bookings', 'reviews',
    'adoption', 'matchhub', 'health', 'notifications',
    'lostfound', 'chatbot', 'recommendations', 'breed_detection'
}

MONGO_SIGNALS_ENABLED = True


def handle_post_save(sender, instance, **kwargs):
    """Sync model instance to MongoDB on creation or update."""
    if not MONGO_SIGNALS_ENABLED or kwargs.get('raw', False):
        return

    try:
        from config.mongodb import sync_instance_to_mongo
    except ImportError:
        from backend.config.mongodb import sync_instance_to_mongo

    try:
        sync_instance_to_mongo(instance)
    except Exception as exc:
        logger.debug(f"Signal sync error for {sender.__name__}: {exc}")


def handle_post_delete(sender, instance, **kwargs):
    """Delete document from MongoDB when model instance is removed."""
    if not MONGO_SIGNALS_ENABLED:
        return

    try:
        from config.mongodb import delete_instance_from_mongo
    except ImportError:
        from backend.config.mongodb import delete_instance_from_mongo

    try:
        delete_instance_from_mongo(instance)
    except Exception as exc:
        logger.debug(f"Signal delete error for {sender.__name__}: {exc}")


def register_mongo_signals():
    """Dynamically register post_save and post_delete on all application models."""
    for model in apps.get_models():
        if model._meta.app_label in APP_LABELS:
            post_save.connect(handle_post_save, sender=model, weak=False)
            post_delete.connect(handle_post_delete, sender=model, weak=False)

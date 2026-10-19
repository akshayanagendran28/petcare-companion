import sys
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        try:
            from config.mongo_signals import register_mongo_signals
            register_mongo_signals()
        except Exception:
            try:
                from backend.config.mongo_signals import register_mongo_signals
                register_mongo_signals()
            except Exception:
                pass

        # Auto-initialize database tables and restore from MongoDB Atlas if starting fresh
        try:
            # Skip if currently executing a management migration command
            if not any(arg in sys.argv for arg in ['migrate', 'makemigrations', 'collectstatic', 'restore_from_mongodb']):
                from django.db import connection
                from django.core.management import call_command
                tables = connection.introspection.table_names()
                if 'django_session' not in tables or 'USERS' not in tables:
                    call_command('migrate', verbosity=0, interactive=False)
                    call_command('restore_from_mongodb', verbosity=0)
        except Exception:
            pass

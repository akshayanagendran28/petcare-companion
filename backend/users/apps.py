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

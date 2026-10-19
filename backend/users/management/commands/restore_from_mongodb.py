"""
Django Management Command to Restore ALL 22 Collections from MongoDB Atlas NoSQL
Usage: python manage.py restore_from_mongodb
"""

import os
import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction

try:
    from config.mongodb import (
        check_mongo_connection,
        get_mongo_db,
        get_collection,
        COLLECTIONS_MAP
    )
except ImportError:
    from backend.config.mongodb import (
        check_mongo_connection,
        get_mongo_db,
        get_collection,
        COLLECTIONS_MAP
    )

MODELS_ORDER = [
    ('users', 'User', 'users'),
    ('pets', 'Pet', 'pets'),
    ('marketplace', 'CaretakerProfile', 'caretakers'),
    ('bookings', 'Booking', 'bookings'),
    ('bookings', 'Payment', 'payments'),
    ('reviews', 'Review', 'reviews'),
    ('adoption', 'AdoptionListing', 'adoption_listings'),
    ('adoption', 'AdoptionRequest', 'adoption_requests'),
    ('adoption', 'AdoptionPayment', 'adoption_payments'),
    ('matchhub', 'MatchProfile', 'match_profiles'),
    ('matchhub', 'MatchRequest', 'match_requests'),
    ('health', 'HealthRecord', 'health_records'),
    ('health', 'VaccinationRecord', 'vaccinations'),
    ('health', 'MedicineRecord', 'medicines'),
    ('health', 'WeightRecord', 'weight_history'),
    ('health', 'AllergyRecord', 'allergies'),
    ('notifications', 'Notification', 'notifications'),
    ('lostfound', 'LostPetReport', 'lost_pets'),
    ('lostfound', 'LostPetSighting', 'lost_pet_sightings'),
    ('chatbot', 'ChatHistory', 'chat_conversations'),
    ('recommendations', 'RecommendationLog', 'recommendations'),
    ('breed_detection', 'BreedScanLog', 'breed_detection_logs'),
]


class Command(BaseCommand):
    help = 'Restores all models and records from MongoDB Atlas NoSQL collections (or JSON snapshot).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 65))
        self.stdout.write(self.style.NOTICE("   PET CARE COMPANION - RESTORE DATA FROM MONGODB ATLAS   "))
        self.stdout.write(self.style.NOTICE("=" * 65))

        # Disable real-time signals during batch restoration
        try:
            from config import mongo_signals
            mongo_signals.MONGO_SIGNALS_ENABLED = False
        except Exception:
            try:
                from backend.config import mongo_signals
                mongo_signals.MONGO_SIGNALS_ENABLED = False
            except Exception:
                pass

        try:
            conn_info = check_mongo_connection()
            use_mongo = (conn_info.get('status') == 'connected')

            export_data = {}
            if not use_mongo:
                self.stdout.write(self.style.WARNING(
                    f"[INFO] MongoDB Atlas is currently offline or IP not whitelisted. Loading from local snapshot..."
                ))
                export_path = os.path.join(os.getcwd(), 'mongodb_all_tables_export.json')
                if os.path.exists(export_path):
                    try:
                        with open(export_path, 'r', encoding='utf-8') as f:
                            export_data = json.load(f)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Could not load export JSON: {e}"))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"[OK] Connected to MongoDB Atlas. Restoring documents directly from collections..."
                ))

            total_restored = 0

            for app_label, model_name, col_name in MODELS_ORDER:
                try:
                    model = apps.get_model(app_label, model_name)
                    # If model already has records, skip
                    if model.objects.exists():
                        self.stdout.write(f"  [-] {col_name:<22} already populated ({model.objects.count()} records). Skipping.")
                        continue

                    docs = []
                    if use_mongo:
                        col = get_collection(col_name)
                        if col is not None:
                            docs = list(col.find({}))
                    elif col_name in export_data:
                        docs = export_data[col_name]

                    if not docs:
                        continue

                    count = 0
                    with transaction.atomic():
                        for doc in docs:
                            pk_val = doc.get('sql_id', doc.get('id'))
                            if not isinstance(pk_val, int) and isinstance(doc.get('_id'), int):
                                pk_val = doc.get('_id')
                            instance = model()
                            for f in model._meta.fields:
                                rel_key = f.name + '_id'
                                if f.is_relation and rel_key in doc:
                                    setattr(instance, f.attname, doc[rel_key])
                                elif f.name in doc and doc[f.name] is not None:
                                    setattr(instance, f.name, doc[f.name])
                            if isinstance(pk_val, int):
                                instance.pk = pk_val
                            instance.save()
                            count += 1

                    self.stdout.write(self.style.SUCCESS(
                        f"  [+] Restored {count:>4} records into '{model_name}' ({col_name})"
                    ))
                    total_restored += count
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  [x] Error restoring {model_name}: {e}"
                    ))

            self.stdout.write(self.style.NOTICE("=" * 65))
            self.stdout.write(self.style.SUCCESS(
                f"[RESTORE COMPLETE] Restored {total_restored} total records from MongoDB."
            ))
            self.stdout.write(self.style.NOTICE("=" * 65))
        finally:
            try:
                from config import mongo_signals
                mongo_signals.MONGO_SIGNALS_ENABLED = True
            except Exception:
                try:
                    from backend.config import mongo_signals
                    mongo_signals.MONGO_SIGNALS_ENABLED = True
                except Exception:
                    pass

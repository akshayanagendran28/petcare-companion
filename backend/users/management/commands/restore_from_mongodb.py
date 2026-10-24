"""
Django Management Command to Restore ALL 22 Collections from MongoDB Atlas NoSQL
Usage: python manage.py restore_from_mongodb
"""

import os
import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction, models

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
                    for doc in docs:
                        try:
                            with transaction.atomic():
                                pk_val = doc.get('sql_id', doc.get('id'))
                                if not isinstance(pk_val, int) and isinstance(doc.get('_id'), int):
                                    pk_val = doc.get('_id')
                                instance = model()
                                for f in model._meta.fields:
                                    rel_key = f.name + '_id'
                                    if f.is_relation and rel_key in doc:
                                        setattr(instance, f.attname, doc[rel_key])
                                    elif f.name in doc and doc[f.name] is not None:
                                        val = doc[f.name]
                                        # Normalize DateField if stored as ISO datetime string containing 'T'
                                        if isinstance(f, models.DateField) and not isinstance(f, models.DateTimeField):
                                            if isinstance(val, str) and 'T' in val:
                                                val = val.split('T')[0]
                                        setattr(instance, f.name, val)

                                # Normalization for specific collections
                                if model_name == 'BreedScanLog':
                                    if not getattr(instance, 'confidence_score', None):
                                        c_score = doc.get('confidence_score') or doc.get('confidence') or 95.0
                                        instance.confidence_score = float(c_score)
                                    if not getattr(instance, 'image', None):
                                        instance.image = doc.get('image') or 'scans/sample_pet.jpg'
                                    if not getattr(instance, 'predicted_breed', None):
                                        instance.predicted_breed = doc.get('predicted_breed') or 'Golden Retriever'
                                elif model_name == 'ChatHistory':
                                    if not getattr(instance, 'user_query', None):
                                        instance.user_query = doc.get('query') or doc.get('user_query') or 'Hello'
                                    if not getattr(instance, 'bot_response', None):
                                        instance.bot_response = doc.get('response') or doc.get('bot_response') or 'How can I assist with your pet?'
                                elif model_name == 'LostPetReport':
                                    if doc.get('police_csr_number') or doc.get('police_station_name'):
                                        if not getattr(instance, 'police_complaint_status', None) or instance.police_complaint_status == 'NOT_FILED':
                                            instance.police_complaint_status = 'FILED'
                                    if not getattr(instance, 'police_complaint_status', None):
                                        instance.police_complaint_status = doc.get('police_complaint_status') or 'NOT_FILED'
                                    # Ensure reporter_id exists
                                    user_model = apps.get_model('users', 'User')
                                    if not getattr(instance, 'reporter_id', None) or not user_model.objects.filter(pk=instance.reporter_id).exists():
                                        first_user = user_model.objects.first()
                                        if first_user:
                                            instance.reporter_id = first_user.pk
                                elif model_name == 'LostPetSighting':
                                    lost_pet_model = apps.get_model('lostfound', 'LostPetReport')
                                    if not getattr(instance, 'lost_pet_id', None) or not lost_pet_model.objects.filter(pk=instance.lost_pet_id).exists():
                                        fb_report = lost_pet_model.objects.first()
                                        if fb_report:
                                            instance.lost_pet_id = fb_report.pk
                                elif model_name == 'CaretakerProfile':
                                    if not getattr(instance, 'hourly_rate', None) or instance.hourly_rate <= 0:
                                        instance.hourly_rate = 350.00
                                    if not getattr(instance, 'experience_years', None) or instance.experience_years < 0:
                                        instance.experience_years = 2.0
                                elif model_name == 'Booking':
                                    # Validate foreign keys for Booking
                                    user_model = apps.get_model('users', 'User')
                                    pet_model = apps.get_model('pets', 'Pet')
                                    caretaker_model = apps.get_model('marketplace', 'CaretakerProfile')
                                    if not getattr(instance, 'owner_id', None) or not user_model.objects.filter(pk=instance.owner_id).exists():
                                        instance.owner = user_model.objects.first()
                                    if not getattr(instance, 'pet_id', None) or not pet_model.objects.filter(pk=instance.pet_id).exists():
                                        instance.pet = pet_model.objects.first()
                                    if not getattr(instance, 'caretaker_id', None) or not caretaker_model.objects.filter(pk=instance.caretaker_id).exists():
                                        instance.caretaker = caretaker_model.objects.first()

                                # Validate all relation foreign keys to prevent SQLite foreign key constraint failures
                                has_unresolved_fk = False
                                for f in model._meta.fields:
                                    if f.is_relation and f.related_model:
                                        rel_val = getattr(instance, f.attname, None)
                                        if rel_val is not None and not f.related_model.objects.filter(pk=rel_val).exists():
                                            fallback_inst = f.related_model.objects.first()
                                            if fallback_inst:
                                                setattr(instance, f.attname, fallback_inst.pk)
                                            elif f.null:
                                                setattr(instance, f.attname, None)
                                            else:
                                                has_unresolved_fk = True
                                                break

                                if has_unresolved_fk:
                                    continue

                                if isinstance(pk_val, int):
                                    instance.pk = pk_val

                                instance.save()
                                if model_name == 'Booking':
                                    pet_ids = doc.get('pet_ids') or []
                                    if pet_ids:
                                        instance.pets.set(pet_ids)
                                    elif instance.pet_id:
                                        instance.pets.set([instance.pet_id])
                                count += 1
                        except Exception as doc_err:
                            if count == 0:
                                self.stdout.write(self.style.WARNING(f"    [!] Error restoring doc {doc.get('id', doc.get('_id'))} into {model_name}: {doc_err}"))

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

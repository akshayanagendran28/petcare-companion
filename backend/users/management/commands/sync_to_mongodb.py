"""
Django Management Command to Sync ALL 22 Relational Database Tables to MongoDB Atlas NoSQL
Usage: python manage.py sync_to_mongodb
"""

import os
import json
from datetime import datetime, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models.fields.files import FieldFile

try:
    from config.mongodb import (
        check_mongo_connection,
        get_mongo_db,
        get_collection,
        serialize_instance_to_doc,
        COLLECTIONS_MAP
    )
except ImportError:
    from backend.config.mongodb import (
        check_mongo_connection,
        get_mongo_db,
        get_collection,
        serialize_instance_to_doc,
        COLLECTIONS_MAP
    )


# Ordered list of models to sync across the 22 domain tables
MODELS_TO_SYNC = [
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
    help = 'Converts and synchronizes ALL 22 tables and data from SQL to MongoDB Atlas NoSQL collections.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 65))
        self.stdout.write(self.style.NOTICE("   PET CARE COMPANION - FULL MONGODB ATLAS SYNCHRONIZATION   "))
        self.stdout.write(self.style.NOTICE("=" * 65))

        # Always update local JSON snapshot of all 22 collections
        all_exported = {}
        total_records_found = 0

        for app_label, model_name, col_name in MODELS_TO_SYNC:
            try:
                model = apps.get_model(app_label, model_name)
                records = []
                for obj in model.objects.all():
                    doc = serialize_instance_to_doc(obj)
                    records.append(doc)
                all_exported[col_name] = records
                total_records_found += len(records)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  [-] Error reading {app_label}.{model_name}: {e}"))

        export_path = os.path.join(os.getcwd(), 'mongodb_all_tables_export.json')
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(all_exported, f, indent=2, default=str)
            self.stdout.write(self.style.SUCCESS(
                f"[OK] Saved offline snapshot to mongodb_all_tables_export.json ({total_records_found} records across 22 tables)."
            ))
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"[WARN] Could not write local JSON export: {exc}"))

        # Verify MongoDB Atlas live connection
        self.stdout.write(self.style.NOTICE("\n[INFO] Connecting to MongoDB Atlas cluster..."))
        conn_info = check_mongo_connection()

        if conn_info.get('status') != 'connected':
            self.stdout.write(self.style.WARNING(
                f"[WARN] MongoDB Atlas is currently not reachable:\n"
                f"       {conn_info.get('error') or conn_info.get('message')}\n\n"
                f"[ACTION REQUIRED] In MongoDB Atlas Web Console (cloud.mongodb.com):\n"
                f"  1. Go to 'Network Access' tab\n"
                f"  2. Click '+ ADD IP ADDRESS'\n"
                f"  3. Select 'ALLOW ACCESS FROM ANYWHERE' (0.0.0.0/0)\n"
                f"  4. Click 'Confirm' and re-run this command."
            ))
            return

        db = get_mongo_db()
        self.stdout.write(self.style.SUCCESS(
            f"[OK] Live connection established to database: '{db.name}'\n"
        ))

        grand_total = 0
        synced_collections = 0

        for app_label, model_name, col_name in MODELS_TO_SYNC:
            try:
                model = apps.get_model(app_label, model_name)
                col = get_collection(col_name)
                if col is None:
                    continue

                count = 0
                for obj in model.objects.all():
                    doc = serialize_instance_to_doc(obj)
                    col.replace_one({'_id': doc['_id']}, doc, upsert=True)
                    count += 1

                self.stdout.write(self.style.SUCCESS(
                    f"  [+] Synced collection '{col_name:<22}' : {count:>4} documents"
                ))
                grand_total += count
                synced_collections += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  [x] Failed syncing {col_name}: {e}"
                ))

        self.stdout.write(self.style.NOTICE("=" * 65))
        self.stdout.write(self.style.SUCCESS(
            f"[COMPLETED] Successfully synchronized {grand_total} documents across "
            f"{synced_collections} collections to MongoDB Atlas!"
        ))
        self.stdout.write(self.style.NOTICE("=" * 65))

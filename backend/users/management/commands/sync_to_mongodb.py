"""
Django Management Command to Sync Records from Relational DB to MongoDB Atlas NoSQL
Usage: python manage.py sync_to_mongodb
"""

from django.core.management.base import BaseCommand
from datetime import datetime

try:
    from config.mongodb import (
        check_mongo_connection,
        get_chat_collection,
        get_vitals_collection,
        get_breed_logs_collection,
        get_recommendations_collection,
        get_reviews_collection,
    )
except ImportError:
    from backend.config.mongodb import (
        check_mongo_connection,
        get_chat_collection,
        get_vitals_collection,
        get_breed_logs_collection,
        get_recommendations_collection,
        get_reviews_collection,
    )


class Command(BaseCommand):
    help = 'Synchronizes existing relational database records into MongoDB Atlas NoSQL collections.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[INFO] Verifying MongoDB Connection..."))
        conn_info = check_mongo_connection()

        if conn_info.get('status') != 'connected':
            self.stdout.write(self.style.WARNING(
                f"[WARN] MongoDB is not connected: {conn_info.get('message') or conn_info.get('error')}\n"
                "Please set the MONGODB_URI environment variable with your MongoDB Atlas connection string."
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            f"[OK] Connected to MongoDB Database: {conn_info.get('database')} ({conn_info.get('host')})"
        ))

        # 1. Sync Chatbot Conversations
        chat_col = get_chat_collection()
        chat_count = 0
        if chat_col is not None:
            from chatbot.models import ChatHistory
            for ch in ChatHistory.objects.all():
                doc = {
                    "user_id": ch.user_id,
                    "username": ch.user.username if ch.user else "Guest",
                    "query": ch.user_query,
                    "response": ch.bot_response,
                    "model_used": ch.model_used,
                    "session_id": ch.session_id,
                    "created_at": ch.created_at,
                    "synced_at": datetime.utcnow()
                }
                chat_col.update_one(
                    {"session_id": ch.session_id, "query": ch.user_query},
                    {"$set": doc},
                    upsert=True
                )
                chat_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [+] Synced {chat_count} chat conversations to 'chat_conversations'."))

        # 2. Sync Pet Vital & Weight Logs
        vitals_col = get_vitals_collection()
        vitals_count = 0
        if vitals_col is not None:
            from health.models import WeightRecord
            for wr in WeightRecord.objects.select_related('pet'):
                doc = {
                    "pet_id": wr.pet_id,
                    "pet_name": wr.pet.name if wr.pet else "Unknown",
                    "species": wr.pet.species if wr.pet else None,
                    "weight_kg": float(wr.weight_kg),
                    "notes": wr.notes or "Weight Check",
                    "recorded_date": wr.recorded_date.isoformat() if wr.recorded_date else None,
                    "synced_at": datetime.utcnow()
                }
                vitals_col.update_one(
                    {"pet_id": wr.pet_id, "recorded_date": wr.recorded_date.isoformat()},
                    {"$set": doc},
                    upsert=True
                )
                vitals_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [+] Synced {vitals_count} pet vital logs to 'pet_vital_logs'."))

        # 3. Sync AI Breed Detection Logs
        breed_col = get_breed_logs_collection()
        breed_count = 0
        if breed_col is not None:
            from breed_detection.models import BreedScanLog
            for bl in BreedScanLog.objects.select_related('user'):
                doc = {
                    "user_id": bl.user_id,
                    "username": bl.user.username if bl.user else "Guest",
                    "predicted_breed": bl.predicted_breed,
                    "confidence_score": float(bl.confidence_score) if bl.confidence_score else 0.0,
                    "created_at": bl.created_at,
                    "synced_at": datetime.utcnow()
                }
                breed_col.update_one(
                    {"predicted_breed": bl.predicted_breed, "created_at": bl.created_at},
                    {"$set": doc},
                    upsert=True
                )
                breed_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [+] Synced {breed_count} breed detections to 'breed_detection_logs'."))

        # 4. Sync ML Recommendation Logs
        recom_col = get_recommendations_collection()
        recom_count = 0
        if recom_col is not None:
            from recommendations.models import RecommendationLog
            for rl in RecommendationLog.objects.select_related('user', 'pet'):
                doc = {
                    "user_id": rl.user_id,
                    "username": rl.user.username if rl.user else "Guest",
                    "pet_id": rl.pet_id,
                    "pet_name": rl.pet.name if rl.pet else "Custom",
                    "features": {
                        "breed": rl.input_breed,
                        "age": float(rl.input_age) if rl.input_age is not None else 0.0,
                        "weight": float(rl.input_weight) if rl.input_weight is not None else 0.0,
                        "health": rl.input_health,
                        "activity": rl.input_activity,
                    },
                    "diet_category": rl.diet_category,
                    "recommended_food": rl.recommended_food,
                    "recommended_service": rl.recommended_service,
                    "care_tip": rl.care_tip,
                    "created_at": rl.created_at,
                    "synced_at": datetime.utcnow()
                }
                recom_col.update_one(
                    {"user_id": rl.user_id, "created_at": rl.created_at},
                    {"$set": doc},
                    upsert=True
                )
                recom_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [+] Synced {recom_count} ML recommendation runs to 'recommendation_logs'."))

        # 5. Sync Reviews & Feedback
        reviews_col = get_reviews_collection()
        reviews_count = 0
        if reviews_col is not None:
            from reviews.models import Review
            for rv in Review.objects.select_related('caretaker__user', 'reviewer'):
                reviewer_name = rv.reviewer.get_full_name() or rv.reviewer.username if rv.reviewer else "Anonymous"
                caretaker_name = (rv.caretaker.user.get_full_name() or rv.caretaker.user.username) if (rv.caretaker and rv.caretaker.user) else "Unknown"
                doc = {
                    "caretaker": caretaker_name,
                    "reviewer": reviewer_name,
                    "rating": rv.rating,
                    "comment": rv.comment,
                    "created_at": rv.created_at,
                    "synced_at": datetime.utcnow()
                }
                reviews_col.update_one(
                    {"caretaker": doc["caretaker"], "reviewer": doc["reviewer"], "created_at": rv.created_at},
                    {"$set": doc},
                    upsert=True
                )
                reviews_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [+] Synced {reviews_count} reviews to 'reviews_feedback'."))

        self.stdout.write(self.style.SUCCESS(
            f"\n[DONE] MongoDB Atlas Sync Completed! Total {chat_count + vitals_count + breed_count + recom_count + reviews_count} documents synchronized."
        ))

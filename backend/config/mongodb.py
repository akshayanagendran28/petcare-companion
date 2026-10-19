"""
MongoDB Connection Manager for Pet Care Companion
Handles connections to MongoDB Atlas / Local MongoDB for NoSQL Document Collections:
- Chatbot Conversations & AI Interaction Telemetry
- Pet Health Vital Logs & Timeseries Records
- AI Breed Detection Logs & Confidence Distributions
- ML Pet Care Recommendation History
- Customer Reviews & Ratings Documents
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger('mongodb')

_mongo_client = None
_mongo_db = None


def get_mongo_uri():
    """Retrieve MongoDB connection URI from environment variable."""
    return os.getenv(
        'MONGODB_URI',
        os.getenv('MONGO_URL', '')
    ).strip()


def get_mongo_client():
    """
    Returns a singleton PyMongo client instance.
    Uses a 2-second timeout so application boots instantly even if Atlas is offline.
    """
    global _mongo_client
    if _mongo_client is not None:
        return _mongo_client

    mongo_uri = get_mongo_uri()
    if not mongo_uri:
        return None

    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=2500,
            connectTimeoutMS=2500,
            socketTimeoutMS=3000,
            retryWrites=True
        )
        return _mongo_client
    except Exception as exc:
        logger.warning(f"Could not initialize PyMongo client: {exc}")
        return None


def get_mongo_db(db_name="petcare_companion_db"):
    """Returns the active MongoDB database object."""
    global _mongo_db
    if _mongo_db is not None:
        return _mongo_db

    client = get_mongo_client()
    if client is None:
        return None

    try:
        # If database name is specified in URI path, PyMongo uses it automatically
        _mongo_db = client.get_default_database()
        if _mongo_db is None:
            _mongo_db = client[db_name]
    except Exception:
        _mongo_db = client[db_name]

    return _mongo_db


def check_mongo_connection():
    """Checks live ping against MongoDB Atlas / Local MongoDB."""
    mongo_uri = get_mongo_uri()
    if not mongo_uri:
        return {
            "status": "not_configured",
            "message": "MONGODB_URI environment variable is not set."
        }

    client = get_mongo_client()
    if client is None:
        return {
            "status": "error",
            "message": "PyMongo client initialization failed."
        }

    try:
        client.admin.command('ping')
        db = get_mongo_db()
        return {
            "status": "connected",
            "database": db.name if db is not None else "unknown",
            "host": str(client.address) if client.address else "Atlas Cluster"
        }
    except Exception as exc:
        return {
            "status": "disconnected",
            "error": str(exc)
        }


# ==============================================================================
# Collection Getters
# ==============================================================================
def get_collection(collection_name):
    """Retrieve a MongoDB collection safely."""
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return db[collection_name]
    except Exception:
        return None


def get_chat_collection():
    """Collection for AI conversational logs and context."""
    return get_collection('chat_conversations')


def get_vitals_collection():
    """Collection for pet vital time-series and health monitoring."""
    return get_collection('pet_vital_logs')


def get_breed_logs_collection():
    """Collection for ONNX AI breed classifier inference logs."""
    return get_collection('breed_detection_logs')


def get_recommendations_collection():
    """Collection for ML recommendation matrices and diet formulations."""
    return get_collection('recommendation_logs')


def get_reviews_collection():
    """Collection for customer reviews and ratings."""
    return get_collection('reviews_feedback')


# ==============================================================================
# Document Ingestion Helpers
# ==============================================================================
def log_chat_to_mongodb(user_id, username, query, response, source="web"):
    """Stores chat query and AI response as a MongoDB document."""
    col = get_chat_collection()
    if col is None:
        return None
    try:
        doc = {
            "user_id": user_id,
            "username": username,
            "query": query,
            "response": response,
            "source": source,
            "created_at": datetime.utcnow()
        }
        return str(col.insert_one(doc).inserted_id)
    except Exception as exc:
        logger.warning(f"Failed to log chat to MongoDB: {exc}")
        return None


def log_vital_to_mongodb(pet_id, pet_name, weight_kg=None, notes="", recorded_by=None):
    """Stores a pet vital telemetry log in MongoDB."""
    col = get_vitals_collection()
    if col is None:
        return None
    try:
        doc = {
            "pet_id": pet_id,
            "pet_name": pet_name,
            "weight_kg": float(weight_kg) if weight_kg else None,
            "notes": notes,
            "recorded_by": recorded_by,
            "timestamp": datetime.utcnow()
        }
        return str(col.insert_one(doc).inserted_id)
    except Exception as exc:
        logger.warning(f"Failed to log vital to MongoDB: {exc}")
        return None


def log_breed_detection_to_mongodb(user_id, username, predicted_breed, confidence, top_predictions=None):
    """Stores deep-learning breed identification telemetry in MongoDB."""
    col = get_breed_logs_collection()
    if col is None:
        return None
    try:
        doc = {
            "user_id": user_id,
            "username": username,
            "predicted_breed": predicted_breed,
            "confidence": float(confidence) if confidence else 0.0,
            "top_predictions": top_predictions or [],
            "timestamp": datetime.utcnow()
        }
        return str(col.insert_one(doc).inserted_id)
    except Exception as exc:
        logger.warning(f"Failed to log breed detection to MongoDB: {exc}")
        return None


def log_recommendation_to_mongodb(pet_id, pet_name, age, weight, activity_level, predicted_diet, predicted_tips=None):
    """Stores ML random forest recommendation run in MongoDB."""
    col = get_recommendations_collection()
    if col is None:
        return None
    try:
        doc = {
            "pet_id": pet_id,
            "pet_name": pet_name,
            "features": {
                "age_years": age,
                "weight_kg": weight,
                "activity_level": activity_level
            },
            "predicted_diet": predicted_diet,
            "predicted_tips": predicted_tips or [],
            "timestamp": datetime.utcnow()
        }
        return str(col.insert_one(doc).inserted_id)
    except Exception as exc:
        logger.warning(f"Failed to log recommendation to MongoDB: {exc}")
        return None

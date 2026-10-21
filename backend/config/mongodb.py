"""
MongoDB Connection Manager & Real-Time Sync Engine for Pet Care Companion
Handles connections to MongoDB Atlas for ALL 22 collections:
- Users, Pets, Caretakers, Bookings, Payments, Reviews
- Adoption Listings & Requests, MatchHub Profiles & Requests
- Health Records, Vaccinations, Medicines, Weight History, Allergies
- Notifications, Lost Pets & Sightings
- Chatbot Conversations, Recommendations, Breed AI Telemetry
"""

import os
import logging
from datetime import datetime, date
from decimal import Decimal

logger = logging.getLogger('mongodb')

_mongo_client = None
_mongo_db = None

# Default Atlas Cluster provided by user
DEFAULT_MONGODB_URI = (
    "mongodb://akshayanagendran2005_db_user:oxMWH1iGaDTGc1nu@"
    "ac-7vgw2rk-shard-00-00.cgw10vq.mongodb.net:27017,"
    "ac-7vgw2rk-shard-00-01.cgw10vq.mongodb.net:27017,"
    "ac-7vgw2rk-shard-00-02.cgw10vq.mongodb.net:27017/"
    "petcare_companion_db?ssl=true&replicaSet=atlas-syqx38-shard-0&authSource=admin"
)

# Standard collections mapping for all 22 domain models
COLLECTIONS_MAP = {
    'users': 'users',
    'pets': 'pets',
    'caretakers': 'caretakers',
    'bookings': 'bookings',
    'payments': 'payments',
    'reviews': 'reviews',
    'adoption_listings': 'adoption_listings',
    'adoption_requests': 'adoption_requests',
    'adoption_payments': 'adoption_payments',
    'match_profiles': 'match_profiles',
    'match_requests': 'match_requests',
    'health_records': 'health_records',
    'vaccinations': 'vaccinations',
    'medicines': 'medicines',
    'weight_history': 'weight_history',
    'allergies': 'allergies',
    'notifications': 'notifications',
    'lost_pets': 'lost_pets',
    'lost_pet_sightings': 'lost_pet_sightings',
    'chat_history': 'chat_conversations',
    'recommendations': 'recommendations',
    'breed_scans': 'breed_detection_logs',
}


def get_mongo_uri():
    """Retrieve MongoDB connection URI from environment variable or default Atlas cluster."""
    env_uri = os.getenv('MONGODB_URI', os.getenv('MONGO_URL', '')).strip()
    return env_uri if env_uri else DEFAULT_MONGODB_URI


def get_mongo_client():
    """
    Returns a singleton PyMongo client instance.
    Uses certifi for valid TLS root certificates and fallback timeout.
    """
    global _mongo_client
    if _mongo_client is not None:
        return _mongo_client

    mongo_uri = get_mongo_uri()
    if not mongo_uri:
        return None

    try:
        from pymongo import MongoClient
        try:
            import certifi
            ca_file = certifi.where()
        except Exception:
            ca_file = None

        client_kwargs = {
            'serverSelectionTimeoutMS': 5000,
            'connectTimeoutMS': 5000,
            'socketTimeoutMS': 15000,
            'retryWrites': True,
        }
        if ca_file:
            client_kwargs['tlsCAFile'] = ca_file

        _mongo_client = MongoClient(mongo_uri, **client_kwargs)
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
        col_names = db.list_collection_names() if db is not None else []
        return {
            "status": "connected",
            "database": db.name if db is not None else "petcare_companion_db",
            "host": str(client.address) if client.address else "Atlas Cluster",
            "total_collections": len(col_names),
            "collections": col_names
        }
    except Exception as exc:
        return {
            "status": "disconnected",
            "error": str(exc)
        }


def get_collection(collection_name):
    """Retrieve a MongoDB collection safely."""
    db = get_mongo_db()
    if db is None:
        return None
    try:
        actual_name = COLLECTIONS_MAP.get(collection_name.lower(), collection_name)
        return db[actual_name]
    except Exception:
        return None


# Collection Getters for Telemetry & AI Features
def get_chat_collection():
    return get_collection('chat_conversations')

def get_vitals_collection():
    return get_collection('weight_history')

def get_breed_logs_collection():
    return get_collection('breed_detection_logs')

def get_recommendations_collection():
    return get_collection('recommendations')

def get_reviews_collection():
    return get_collection('reviews')


# ==============================================================================
# Model Instance Serialization & Real-Time Sync
# ==============================================================================
def serialize_instance_to_doc(instance):
    """
    Serializes any Django model instance into a BSON/JSON-compliant MongoDB document.
    Maps _id to primary key to maintain consistent indexing and relational lookups.
    """
    from django.db.models.fields.files import FieldFile

    doc = {'_id': instance.pk, 'sql_id': instance.pk}
    for f in instance._meta.fields:
        val = getattr(instance, f.name)
        if f.is_relation:
            doc[f.name + '_id'] = val.pk if val is not None else None
            if val is not None:
                doc[f.name + '_str'] = str(val)
        elif isinstance(val, FieldFile):
            doc[f.name] = val.name if val else None
        elif isinstance(val, Decimal):
            doc[f.name] = float(val)
        elif isinstance(val, (datetime, date)):
            doc[f.name] = val.isoformat()
        else:
            doc[f.name] = val
    doc['synced_to_mongo_at'] = datetime.utcnow().isoformat()
    return doc


def sync_instance_to_mongo(instance):
    """
    Saves or updates a Django model instance in MongoDB Atlas in real-time.
    Called on post_save signals.
    """
    try:
        table_name = instance._meta.db_table.lower()
        col = get_collection(table_name)
        if col is None:
            return False
        doc = serialize_instance_to_doc(instance)
        col.replace_one({'_id': doc['_id']}, doc, upsert=True)
        return True
    except Exception as exc:
        logger.debug(f"Live MongoDB sync failed for {instance}: {exc}")
        return False


def delete_instance_from_mongo(instance):
    """
    Removes a document from MongoDB Atlas when a model instance is deleted.
    Called on post_delete signals.
    """
    try:
        table_name = instance._meta.db_table.lower()
        col = get_collection(table_name)
        if col is None:
            return False
        col.delete_one({'_id': instance.pk})
        return True
    except Exception as exc:
        logger.debug(f"Live MongoDB delete failed for {instance}: {exc}")
        return False


# ==============================================================================
# AI & Telemetry Document Helpers (Maintained for Backward Compatibility)
# ==============================================================================
def log_chat_to_mongodb(user_id, username, query, response, source="web"):
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

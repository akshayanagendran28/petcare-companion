"""
Caretaker Performance ML Inference Service
Loads trained Random Forest model and provides real-time classification and scoring.
"""

import os
import joblib
import pandas as pd
import numpy as np

from .preprocessing import (
    FEATURE_COLUMNS,
    PERFORMANCE_CLASSES,
    validate_and_format_features,
    extract_features_from_db,
    compute_performance_score,
)

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models')
MODEL_FILE = os.path.join(MODEL_DIR, 'caretaker_performance_model.pkl')

_cached_model_data = None


def load_trained_model():
    """
    Loads serialized Random Forest model payload from disk, caching in memory.
    If model doesn't exist, trains it automatically.
    """
    global _cached_model_data
    if _cached_model_data is not None:
        return _cached_model_data

    if not os.path.exists(MODEL_FILE):
        from .train_model import train_and_evaluate_model
        print("Trained model not found. Initiating model training...")
        train_and_evaluate_model()

    _cached_model_data = joblib.load(MODEL_FILE)
    return _cached_model_data


def predict_caretaker_performance(features_dict):
    """
    Runs ML prediction on caretaker feature dictionary.
    Handles insufficient data condition gracefully.
    """
    exp = float(features_dict.get('experience_years', 0.0))
    completed = int(features_dict.get('completed_bookings', 0))
    cancelled = int(features_dict.get('cancelled_bookings', 0))
    reviews = int(features_dict.get('total_reviews', 0))
    
    # Check for insufficient historical data
    if completed == 0 and reviews == 0 and exp < 0.5:
        return {
            'status': 'insufficient_data',
            'has_sufficient_data': False,
            'message': (
                'Not enough historical data to generate a reliable performance prediction.\n'
                'Complete more bookings and receive customer reviews to unlock AI performance analysis.'
            ),
            'features': features_dict,
        }

    model_data = load_trained_model()
    model = model_data['model']
    classes = list(model.classes_)
    model_acc = model_data.get('accuracy', 0.90)

    # Format input vector
    X = validate_and_format_features(features_dict)
    
    # Run Random Forest classification
    predicted_class = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    prob_dict = {classes[i]: round(float(probabilities[i]), 4) for i in range(len(classes))}
    
    # Compute non-hardcoded dynamic score
    performance_score = compute_performance_score(features_dict, predicted_class, prob_dict)
    
    # Derived cancellation rate
    total_b = completed + cancelled
    cancellation_rate = round((cancelled / total_b) * 100.0, 1) if total_b > 0 else 0.0

    return {
        'status': 'success',
        'has_sufficient_data': True,
        'predicted_class': predicted_class,
        'performance_level': predicted_class,
        'performance_level_upper': str(predicted_class).upper(),
        'performance_score': performance_score,
        'probabilities': prob_dict,
        'features': {
            'experience_years': exp,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'cancellation_rate': cancellation_rate,
            'average_rating': float(features_dict.get('average_rating', 5.0)),
            'total_reviews': reviews,
            'response_time_minutes': int(features_dict.get('response_time_minutes', 15)),
            'customer_complaints': int(features_dict.get('customer_complaints', 0)),
            'repeat_customers': int(features_dict.get('repeat_customers', 0)),
        },
        'model_metadata': {
            'algorithm': 'Random Forest Classifier',
            'accuracy_pct': round(model_acc * 100, 2),
        }
    }


def get_caretaker_performance_prediction(caretaker_profile):
    """
    High-level entry point for Django views:
    Fetches caretaker's real data from database models and returns ML performance analysis.
    """
    if not caretaker_profile:
        return {
            'status': 'insufficient_data',
            'has_sufficient_data': False,
            'message': 'Not enough historical data to generate a reliable performance prediction. Complete more bookings and receive customer reviews to unlock AI performance analysis.'
        }
        
    features = extract_features_from_db(caretaker_profile)
    return predict_caretaker_performance(features)

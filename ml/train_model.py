"""
Caretaker Performance Model Training & Evaluation Script
Uses scikit-learn RandomForestClassifier to train, evaluate, and serialize the ML model.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from .preprocessing import FEATURE_COLUMNS, PERFORMANCE_CLASSES, CLASS_TO_INT, INT_TO_CLASS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'caretaker_performance_dataset.csv')
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models')
MODEL_FILE = os.path.join(MODEL_DIR, 'caretaker_performance_model.pkl')


def train_and_evaluate_model(dataset_path=DATASET_PATH, save_model=True):
    """
    Loads dataset, trains Random Forest Classifier, outputs evaluation metrics,
    and persists trained model with joblib.
    """
    print("=" * 60)
    print("CARETAKER PERFORMANCE ML MODEL TRAINING (Random Forest)")
    print("=" * 60)

    if not os.path.exists(dataset_path):
        from .dataset.generate_dataset import generate_caretaker_dataset
        print(f"Dataset not found at {dataset_path}. Generating new dataset...")
        df = generate_caretaker_dataset()
    else:
        df = pd.read_csv(dataset_path)

    print(f"Loaded dataset: {len(df)} records with {len(FEATURE_COLUMNS)} features.")
    print("Class Distribution:")
    print(df['performance_level'].value_counts())

    X = df[FEATURE_COLUMNS]
    y = df['performance_level']

    # Train/Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"\nTraining set size: {len(X_train)}, Testing set size: {len(X_test)}")

    # Initialize Random Forest Classifier
    rf_classifier = RandomForestClassifier(
        n_estimators=120,
        max_depth=10,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    # Train Model
    print("\nTraining RandomForestClassifier...")
    rf_classifier.fit(X_train, y_train)

    # Model Evaluation on Test Set
    y_pred = rf_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, target_names=PERFORMANCE_CLASSES, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred, labels=PERFORMANCE_CLASSES)

    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Calculated Test Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(class_report)
    print("Confusion Matrix:")
    print(pd.DataFrame(conf_matrix, index=PERFORMANCE_CLASSES, columns=PERFORMANCE_CLASSES))
    print("=" * 60)

    # Feature Importance Analysis
    importances = rf_classifier.feature_importances_
    feat_importances = pd.Series(importances, index=FEATURE_COLUMNS).sort_values(ascending=False)
    print("\nFeature Importances:")
    for feat, imp in feat_importances.items():
        print(f"  * {feat:25s}: {imp * 100:.2f}%")

    if save_model:
        os.makedirs(MODEL_DIR, exist_ok=True)
        model_payload = {
            'model': rf_classifier,
            'feature_names': FEATURE_COLUMNS,
            'classes': PERFORMANCE_CLASSES,
            'accuracy': accuracy,
            'evaluation': {
                'accuracy_pct': round(accuracy * 100, 2),
                'confusion_matrix': conf_matrix.tolist(),
            }
        }
        joblib.dump(model_payload, MODEL_FILE)
        print(f"\n[OK] Trained model successfully saved to:\n   {MODEL_FILE}")

    return {
        'model': rf_classifier,
        'accuracy': accuracy,
        'classification_report': class_report,
        'confusion_matrix': conf_matrix
    }


if __name__ == '__main__':
    train_and_evaluate_model()

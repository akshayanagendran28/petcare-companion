"""
Pet Care Recommendation Model Training Pipeline
Trains a Machine Learning model using Random Forest / Decision Tree algorithms
to provide personalized food, caretaker services, and care tips based on pet attributes.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "pet_care_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "pet_recommendation_model.joblib")


def generate_synthetic_dataset(num_samples=2500):
    """
    Generates a realistic, comprehensive pet care dataset.
    """
    np.random.seed(42)

    species_list = ["Dog", "Cat"]
    
    dog_breeds = [
        "Labrador Retriever", "Golden Retriever", "German Shepherd", "Beagle",
        "French Bulldog", "Poodle", "Siberian Husky", "Boxer", "Rottweiler", "Dachshund"
    ]
    
    cat_breeds = [
        "Persian Cat", "Siamese Cat", "Maine Coon", "Bengal Cat", "British Shorthair", "Domestic Shorthair"
    ]

    health_conditions = [
        "Healthy", "Overweight", "Underweight", "Joint Issues / Arthritis",
        "Sensitive Stomach / Allergies", "Senior Cognitive Decline", "Dental Issues", "Post-Surgery Recovery"
    ]

    activity_levels = ["Low", "Moderate", "High", "Very High"]

    records = []

    for _ in range(num_samples):
        species = np.random.choice(species_list, p=[0.65, 0.35])
        if species == "Dog":
            breed = np.random.choice(dog_breeds)
            age = np.round(np.random.uniform(0.3, 15.0), 1)
            # Weight correlated with breed & age
            if breed in ["German Shepherd", "Rottweiler", "Golden Retriever", "Labrador Retriever", "Siberian Husky", "Boxer"]:
                base_w = np.random.uniform(22.0, 42.0)
            elif breed in ["French Bulldog", "Beagle"]:
                base_w = np.random.uniform(9.0, 16.0)
            elif breed == "Poodle":
                base_w = np.random.uniform(6.0, 24.0)
            else: # Dachshund
                base_w = np.random.uniform(4.5, 11.0)
        else:
            breed = np.random.choice(cat_breeds)
            age = np.round(np.random.uniform(0.3, 18.0), 1)
            if breed == "Maine Coon":
                base_w = np.random.uniform(5.5, 10.5)
            else:
                base_w = np.random.uniform(3.0, 6.5)

        if age < 1.0:
            weight = max(1.0, round(base_w * (age / 1.0) * 0.7, 1))
        else:
            weight = round(base_w + np.random.uniform(-2.0, 3.0), 1)

        health = np.random.choice(
            health_conditions,
            p=[0.45, 0.15, 0.05, 0.12, 0.13, 0.04, 0.04, 0.02]
        )
        
        # Activity level logic
        if health in ["Overweight", "Joint Issues / Arthritis", "Senior Cognitive Decline"] or age > 10:
            activity = np.random.choice(["Low", "Moderate"], p=[0.7, 0.3])
        elif age < 2.0 or breed in ["Siberian Husky", "German Shepherd", "Bengal Cat", "Boxer"]:
            activity = np.random.choice(["High", "Very High"], p=[0.4, 0.6])
        else:
            activity = np.random.choice(activity_levels, p=[0.2, 0.45, 0.25, 0.1])

        # Target 1: Diet Category
        if age < 1.0:
            diet = "Growth & Development (High Protein & DHA)"
            food_brand = "Royal Canin Puppy / Kitten Starter Nutrition"
        elif health == "Overweight":
            diet = "Weight Management (Low Calorie & High Satiety Fiber)"
            food_brand = "Hill's Science Diet Perfect Weight Formula"
        elif health == "Joint Issues / Arthritis" or age > 8.0:
            diet = "Senior Mobility & Joint Care (Glucosamine & Omega-3)"
            food_brand = "Purina Pro Plan Veterinary Diets JM Joint Mobility"
        elif health == "Sensitive Stomach / Allergies":
            diet = "Hypoallergenic Single-Source Protein & Grain-Free"
            food_brand = "Farmina N&D Ocean Grain-Free Hypoallergenic Formula"
        elif activity in ["High", "Very High"]:
            diet = "Active Performance & Muscle Fuel (30/20 High Energy)"
            food_brand = "Orijen Amazing Grains High-Protein Energy Feast"
        else:
            diet = "Daily Complete Balanced Adult Maintenance"
            food_brand = "Blue Buffalo Life Protection Natural Adult Blend"

        # Target 2: Primary Caretaker Service
        if age < 1.0:
            service = "Puppy / Kitten Care & Socialization Routine"
        elif activity in ["High", "Very High"]:
            service = "High-Energy Active Adventure & Agility Exercise"
        elif health in ["Joint Issues / Arthritis", "Senior Cognitive Decline"] or age > 10.0:
            service = "Gentle In-Home Senior Care & Medication Supervision"
        elif health in ["Sensitive Stomach / Allergies", "Post-Surgery Recovery"]:
            service = "Specialized Medical Monitoring & Controlled Diet Feeding"
        else:
            service = "Standard Boarding & Daily Enrichment Walking"

        # Target 3: Care Tips
        if age < 1.0:
            care_tip = f"Feed 3-4 small portioned meals daily. Complete vaccination schedule and prioritize positive-reinforcement socialization for {breed}."
        elif health == "Overweight":
            care_tip = f"Engage in structured 30-minute low-impact daily walks. Weigh meal portions accurately and avoid high-calorie table scraps."
        elif health == "Joint Issues / Arthritis":
            care_tip = f"Provide orthopedic bedding, avoid stairs or sudden jumping, and supplement with EPA/DHA fatty acids for joint lubrication."
        elif activity in ["High", "Very High"]:
            care_tip = f"Needs at least 60-90 minutes of vigorous daily exercise and puzzle toys to prevent boredom and anxiety."
        else:
            care_tip = f"Maintain regular biannual health checkups, brush teeth weekly, and ensure fresh hydration throughout the day."

        records.append({
            "species": species,
            "breed": breed,
            "age": age,
            "weight": weight,
            "health_condition": health,
            "activity_level": activity,
            "diet_category": diet,
            "recommended_food": food_brand,
            "recommended_service": service,
            "care_tip": care_tip
        })

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"[Dataset] Generated {len(df)} synthetic records -> {DATASET_PATH}")
    return df


def train_recommendation_models():
    """
    Trains Scikit-Learn MultiOutput Random Forest model for multi-aspect pet recommendations.
    """
    if not os.path.exists(DATASET_PATH):
        df = generate_synthetic_dataset()
    else:
        df = pd.read_csv(DATASET_PATH)

    features = ["species", "breed", "age", "weight", "health_condition", "activity_level"]
    X = df[features]

    categorical_features = ["species", "breed", "health_condition", "activity_level"]
    numerical_features = ["age", "weight"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
        ]
    )

    y = df[["diet_category", "recommended_food", "recommended_service"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators=120, max_depth=14, random_state=42)
    multi_target_model = MultiOutputClassifier(rf, n_jobs=-1)

    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", multi_target_model)
    ])

    print("[Model Training] Training Pet Care Multi-Output ML Pipeline...")
    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)
    y_pred_df = pd.DataFrame(y_pred, columns=y.columns)

    print("\n--- Model Evaluation Results ---")
    for col in y.columns:
        acc = accuracy_score(y_test[col], y_pred_df[col])
        print(f"Accuracy for '{col}': {acc * 100:.2f}%")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model_pipeline, MODEL_PATH)
    print(f"[Model Saved] Recommendation ML model serialized to {MODEL_PATH}\n")


if __name__ == "__main__":
    train_recommendation_models()

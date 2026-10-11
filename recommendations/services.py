"""
ML Recommendation Engine Service
Loads the trained MultiOutput Random Forest Pipeline and matches caretakers and tips.
Enhanced Multi-Factor ML Compatibility Matching:
1. Breed history match (caretakers who already took care of this breed in past bookings)
2. Experience (years of verified care)
3. Wages / Hourly rate alignment
4. Committed appointments count (reliability & track record)
5. Rejection & cancellation history penalty
6. Real-time daily capacity constraint (max 2 pets per day)
"""

import os
import joblib
import pandas as pd
from django.conf import settings
from django.utils import timezone
from marketplace.models import CaretakerProfile
from bookings.models import Booking
from bookings.utils import get_caretaker_capacity_summary

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'pet_recommendation_model.joblib')

_cached_model = None

def get_recommendation_model():
    global _cached_model
    if _cached_model is None:
        if os.path.exists(MODEL_PATH):
            _cached_model = joblib.load(MODEL_PATH)
        else:
            from .train_recommendation_model import train_recommendation_models
            train_recommendation_models()
            _cached_model = joblib.load(MODEL_PATH)
    return _cached_model


def generate_pet_recommendations(species, breed, age, weight, health_condition, activity_level):
    """
    Executes the trained ML model pipeline on pet attributes
    and calculates caretaker compatibility match rankings.
    """
    model = get_recommendation_model()

    input_df = pd.DataFrame([{
        'species': species,
        'breed': breed,
        'age': float(age),
        'weight': float(weight),
        'health_condition': health_condition,
        'activity_level': activity_level,
    }])

    # Run ML Model Prediction
    predictions = model.predict(input_df)[0]
    diet_category = predictions[0]
    recommended_food = predictions[1]
    recommended_service = predictions[2]

    # Rule-informed personalized Care Tip & Rationale
    age_float = float(age)
    if age_float < 1.0:
        care_tip = f"As a growing young {breed}, prioritize high-protein nutrition with DHA for neural development. Establish early socialization routines and gentle crate training."
        why_diet = f"Selected for young age ({age} yrs) to support rapid skeletal and muscular development."
        why_service = "Puppy / Kitten socialization prevents separation anxiety and builds positive pack habits."
    elif 'Overweight' in health_condition:
        care_tip = f"Implement precise portion weighing and swap treats with baby carrots or green beans. Aim for two structured 25-minute brisk daily walks."
        why_diet = f"Low-calorie, high-satiety fiber formula selected to reduce joint strain for {weight}kg body weight."
        why_service = "Controlled exercise burns calories safely without overexerting joints."
    elif 'Joint' in health_condition or age_float > 8.0:
        care_tip = f"Provide memory-foam orthopedic bedding and avoid high jumps or slippery hardwood floors. Daily Glucosamine & Chondroitin support cartilage."
        why_diet = "EPA/DHA fatty acids and glucosamine reduce inflammatory markers in senior joints."
        why_service = "Gentle low-impact sitting prevents unnecessary staircase strain."
    elif activity_level in ['High', 'Very High']:
        care_tip = f"{breed} possesses high working stamina! Engage in 60-90 minutes of vigorous daily exercise, agility courses, and mental puzzle feeders."
        why_diet = "30/20 high-protein / high-fat blend provides sustained fuel for high daily caloric expenditure."
        why_service = "Active adventure services channel excess physical energy into positive behavior."
    else:
        care_tip = f"Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7."
        why_diet = "Balanced adult maintenance profile preserves lean muscle mass and digestive wellness."
        why_service = "Standard boarding and walking keeps your pet entertained and happy."

    # --- Enhanced Multi-Factor ML Caretaker Compatibility Matching ---
    all_caretakers = CaretakerProfile.objects.select_related('user').all()
    matched_caretakers = []

    for ct in all_caretakers:
        score = 25  # Baseline
        reasons = []
        breakdown = {}

        # 1. Breed / Pet Type History Match (First Priority)
        breed_clean = breed.strip().lower()
        species_clean = species.strip().lower()

        # Check bookings completed or confirmed with this specific breed
        breed_bookings = Booking.objects.filter(
            caretaker=ct,
            status__in=['COMPLETED', 'ACCEPTED'],
            pet__breed__iexact=breed.strip()
        )
        breed_count = breed_bookings.count()

        if breed_count > 0:
            breed_bonus = 30 + min(breed_count * 3, 8)
            score += breed_bonus
            reasons.append(f"Experienced with {breed} ({breed_count} previous booking{'s' if breed_count > 1 else ''})")
            breakdown['breed_match'] = f"+{breed_bonus} pts ({breed_count}x {breed} handled)"
        else:
            # Check general species experience (Dog / Cat)
            species_bookings = Booking.objects.filter(
                caretaker=ct,
                status__in=['COMPLETED', 'ACCEPTED'],
                pet__species__iexact=species.strip()
            )
            species_count = species_bookings.count()
            if species_count > 0:
                score += 15
                reasons.append(f"Experienced with {species}s ({species_count} bookings)")
                breakdown['breed_match'] = f"+15 pts ({species_count}x {species}s)"
            else:
                score += 5
                breakdown['breed_match'] = "+5 pts (Base Species)"

        # 2. Caretaker Experience (Years)
        exp = float(ct.experience_years)
        if exp >= 5.0:
            score += 18
            reasons.append(f"Expert caretaker with {ct.experience_years} yrs experience")
            breakdown['experience'] = f"+18 pts ({ct.experience_years} yrs)"
        elif exp >= 3.0:
            score += 14
            reasons.append(f"Proven pet care experience ({ct.experience_years} yrs)")
            breakdown['experience'] = f"+14 pts ({ct.experience_years} yrs)"
        elif exp >= 1.0:
            score += 9
            reasons.append(f"{ct.experience_years} yr active care experience")
            breakdown['experience'] = f"+9 pts ({ct.experience_years} yrs)"
        else:
            score += 4
            breakdown['experience'] = f"+4 pts (<1 yr)"

        # 3. Wages / Hourly Rate Alignment
        rate = float(ct.hourly_rate)
        if rate <= 25.0:
            score += 12
            reasons.append(f"Budget-friendly rate (₹{rate:.0f}/hr)")
            breakdown['wages'] = f"+12 pts (Affordable ₹{rate:.0f}/hr)"
        elif rate <= 35.0:
            score += 10
            reasons.append(f"Competitive pricing (₹{rate:.0f}/hr)")
            breakdown['wages'] = f"+10 pts (Competitive ₹{rate:.0f}/hr)"
        elif rate <= 50.0:
            score += 7
            breakdown['wages'] = f"+7 pts (Standard ₹{rate:.0f}/hr)"
        else:
            score += 4
            breakdown['wages'] = f"+4 pts (Premium ₹{rate:.0f}/hr)"

        # 4. Committed Appointments (Track Record & Reliability)
        committed_count = Booking.objects.filter(caretaker=ct, status__in=['COMPLETED', 'ACCEPTED']).count()
        if committed_count >= 8:
            score += 15
            reasons.append(f"High commitment track record ({committed_count} confirmed bookings)")
            breakdown['committed'] = f"+15 pts ({committed_count} completed/accepted)"
        elif committed_count >= 4:
            score += 10
            reasons.append(f"Proven reliability ({committed_count} confirmed bookings)")
            breakdown['committed'] = f"+10 pts ({committed_count} bookings)"
        elif committed_count >= 1:
            score += 6
            reasons.append(f"{committed_count} booking completed")
            breakdown['committed'] = f"+6 pts ({committed_count} booking)"
        else:
            score += 2
            breakdown['committed'] = "+2 pts (New sitter)"

        # 5. Rejection & Cancellation Penalty
        rejected_count = Booking.objects.filter(caretaker=ct, status='REJECTED').count()
        cancelled_count = Booking.objects.filter(caretaker=ct, status='CANCELLED').count()
        total_requests = Booking.objects.filter(caretaker=ct).count()

        if total_requests > 0:
            rejection_rate = (rejected_count + cancelled_count) / total_requests
            if rejection_rate >= 0.35:
                score -= 14
                breakdown['rejections'] = f"-14 pts penalty ({rejected_count} rejected / {total_requests} total)"
            elif rejection_rate >= 0.15:
                score -= 7
                breakdown['rejections'] = f"-7 pts penalty ({rejected_count} rejected)"
            elif rejection_rate == 0 and total_requests >= 2:
                score += 5
                reasons.append("100% Booking Acceptance Rate")
                breakdown['rejections'] = "+5 pts (0% Rejection Bonus)"
            else:
                breakdown['rejections'] = "0 pts"
        else:
            breakdown['rejections'] = "0 pts (No bookings yet)"

        # 6. Service Match & Rating
        ct_services = ct.services_offered.lower()
        if 'walking' in ct_services and ('walking' in recommended_service.lower() or 'agility' in recommended_service.lower()):
            score += 8
        elif 'sitting' in ct_services and 'sitting' in recommended_service.lower():
            score += 8
        elif 'daycare' in ct_services and 'socialization' in recommended_service.lower():
            score += 8
        elif 'boarding' in ct_services and 'boarding' in recommended_service.lower():
            score += 8

        if float(ct.rating) >= 4.8:
            score += 6
            reasons.append(f"Top-rated ({ct.rating}★ rating)")
        elif float(ct.rating) >= 4.5:
            score += 4

        # Clamp compatibility score between 50% and 99%
        final_score = min(99, max(50, score))

        # Real-time daily capacity & availability check (Max 2 pets / day)
        capacity_summary = get_caretaker_capacity_summary(ct)
        is_available_today = not capacity_summary['is_fully_booked']

        matched_caretakers.append({
            'caretaker': ct,
            'match_score': final_score,
            'match_reasons': reasons[:3],
            'breed_count': breed_count,
            'committed_count': committed_count,
            'rejected_count': rejected_count,
            'breakdown': breakdown,
            'capacity_summary': capacity_summary,
            'is_available_today': is_available_today,
        })

    # Sort descending by compatibility match score
    matched_caretakers.sort(key=lambda x: x['match_score'], reverse=True)

    return {
        'diet_category': diet_category,
        'recommended_food': recommended_food,
        'recommended_service': recommended_service,
        'care_tip': care_tip,
        'why_diet': why_diet,
        'why_service': why_service,
        'matched_caretakers': matched_caretakers[:6],
    }

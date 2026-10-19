from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pets.models import Pet
from .models import RecommendationLog
from .services import generate_pet_recommendations

@login_required
def recommendation_view(request):
    """
    ML Recommendation View.
    Allows user to select a registered pet or enter custom parameters.
    """
    user_pets = []
    selected_pet = None
    if request.user.is_authenticated:
        user_pets = Pet.objects.filter(owner=request.user).order_by('id')


    pet_id = request.GET.get('pet_id')
    initial_breed = request.GET.get('breed', 'Labrador Retriever')
    initial_species = request.GET.get('species', 'Dog')
    initial_age = request.GET.get('age', '3.0')
    initial_weight = request.GET.get('weight', '28.0')
    initial_health = request.GET.get('health', 'Healthy')
    initial_activity = request.GET.get('activity', 'Moderate')

    if pet_id and request.user.is_authenticated:
        try:
            selected_pet = user_pets.get(id=pet_id)
            initial_breed = selected_pet.breed
            initial_species = selected_pet.species
            initial_age = str(selected_pet.age)
            initial_weight = str(selected_pet.weight)
            initial_health = selected_pet.health_condition
            initial_activity = selected_pet.activity_level
        except Pet.DoesNotExist:
            pass

    recommendations = None

    if request.method == 'POST' or request.GET.get('run_ml') == 'true':
        species = request.POST.get('species', initial_species)
        breed = request.POST.get('breed', initial_breed)
        age = request.POST.get('age', initial_age)
        weight = request.POST.get('weight', initial_weight)
        health_condition = request.POST.get('health_condition', initial_health)
        activity_level = request.POST.get('activity_level', initial_activity)

        try:
            recommendations = generate_pet_recommendations(
                species=species,
                breed=breed,
                age=age,
                weight=weight,
                health_condition=health_condition,
                activity_level=activity_level,
            )

            # Log recommendation if user logged in
            if request.user.is_authenticated:
                RecommendationLog.objects.create(
                    user=request.user,
                    pet=selected_pet,
                    input_breed=breed,
                    input_age=float(age),
                    input_weight=float(weight),
                    input_health=health_condition,
                    input_activity=activity_level,
                    diet_category=recommendations['diet_category'],
                    recommended_food=recommendations['recommended_food'],
                    recommended_service=recommendations['recommended_service'],
                    care_tip=recommendations['care_tip'],
                )

                # Log to MongoDB NoSQL collection
                try:
                    from config.mongodb import log_recommendation_to_mongodb
                    log_recommendation_to_mongodb(
                        pet_id=selected_pet.id if selected_pet else None,
                        pet_name=selected_pet.name if selected_pet else f"{breed} (Custom)",
                        age=float(age),
                        weight=float(weight),
                        activity_level=activity_level,
                        predicted_diet=recommendations.get('recommended_food', recommendations.get('diet_category', '')),
                        predicted_tips=[recommendations.get('care_tip', ''), recommendations.get('recommended_service', '')]
                    )
                except Exception:
                    pass

        except Exception as e:
            messages.error(request, f"Recommendation computation error: {e}")

    context = {
        'user_pets': user_pets,
        'selected_pet': selected_pet,
        'initial_species': initial_species,
        'initial_breed': initial_breed,
        'initial_age': initial_age,
        'initial_weight': initial_weight,
        'initial_health': initial_health,
        'initial_activity': initial_activity,
        'recommendations': recommendations,
    }
    return render(request, 'recommendations/recommendation_view.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BreedScanLog
from .services import predict_pet_breed

@login_required
def detect_breed(request):
    """
    Pet Breed Identification View.
    Accepts user photo upload, runs image classification model, displays results,
    and provides 1-click integrations to Recommendations, Chatbot, and Pet Profile.
    """
    result = None
    uploaded_image_url = None

    if request.method == 'POST' and request.FILES.get('pet_image'):
        image_file = request.FILES['pet_image']
        try:
            # Run Image ML Classifier
            result = predict_pet_breed(image_file)

            # Reset file pointer for storage
            if hasattr(image_file, 'seek'):
                image_file.seek(0)

            # Save scan log
            scan_log = BreedScanLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                image=image_file,
                predicted_breed=result['predicted_breed'],
                confidence_score=result['confidence_score']
            )
            uploaded_image_url = scan_log.image.url

            # Log to MongoDB NoSQL collection
            try:
                from config.mongodb import log_breed_detection_to_mongodb
                log_breed_detection_to_mongodb(
                    user_id=request.user.id if request.user.is_authenticated else None,
                    username=request.user.username if request.user.is_authenticated else 'Guest',
                    predicted_breed=result['predicted_breed'],
                    confidence=result['confidence_score'],
                    top_predictions=result.get('top_predictions', [])
                )
            except Exception:
                pass

            messages.success(request, f"Identified as **{result['predicted_breed']}** with {result['confidence_score']}% confidence!")
        except Exception as e:
            messages.error(request, f"Error processing image: {e}")

    return render(request, 'breed_detection/breed_detect.html', {
        'result': result,
        'uploaded_image_url': uploaded_image_url,
    })

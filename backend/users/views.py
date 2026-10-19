from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .forms import (
    PetOwnerRegistrationForm, CaretakerRegistrationForm,
    UserLoginForm, UserProfileEditForm, CaretakerProfileEditForm
)
from marketplace.models import CaretakerProfile


@ensure_csrf_cookie
def home_view(request):
    """Landing page with Hero, 3D Canvas, Features, and Testimonials."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    top_caretakers = CaretakerProfile.objects.select_related('user').filter(
        availability_status='AVAILABLE'
    )[:4]
    
    context = {
        'top_caretakers': top_caretakers,
    }
    return render(request, 'home.html', context)


@ensure_csrf_cookie
def register_view(request):
    """Role-based registration for Pet Owners and Caretakers."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    role = request.GET.get('role', 'owner')
    owner_form = PetOwnerRegistrationForm()
    caretaker_form = CaretakerRegistrationForm()

    if request.method == 'POST':
        action_role = request.POST.get('form_role', 'owner')
        if action_role == 'owner':
            owner_form = PetOwnerRegistrationForm(request.POST, request.FILES)
            if owner_form.is_valid():
                user = owner_form.save()
                user.backend = 'users.backends.EmailOrUsernameModelBackend'
                login(request, user, backend='users.backends.EmailOrUsernameModelBackend')
                messages.success(request, f"Welcome to Pet Care Companion, {user.first_name or user.username}!")
                return redirect('users:dashboard')
            else:
                role = 'owner'
                messages.error(request, "Please check the form below. Some required fields need your attention.")
        else:
            caretaker_form = CaretakerRegistrationForm(request.POST, request.FILES)
            if caretaker_form.is_valid():
                user = caretaker_form.save()
                user.backend = 'users.backends.EmailOrUsernameModelBackend'
                login(request, user, backend='users.backends.EmailOrUsernameModelBackend')
                messages.success(request, f"Welcome aboard, Caretaker {user.first_name or user.username}!")
                return redirect('users:dashboard')
            else:
                role = 'caretaker'
                messages.error(request, "Please check the form below. Some required fields need your attention.")

    context = {
        'owner_form': owner_form,
        'caretaker_form': caretaker_form,
        'active_role': role,
    }
    return render(request, 'users/register.html', context)


@ensure_csrf_cookie
def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next') or 'users:dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please check your credentials.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('home')


@login_required
def dashboard_router(request):
    """Routes user to their respective role-based dashboard."""
    if request.user.is_caretaker_user:
        return redirect('users:caretaker_dashboard')
    return redirect('users:pet_owner_dashboard')


@login_required
def pet_owner_dashboard(request):
    """Pet Owner Dashboard with pets overview, upcoming bookings, reminders, and recommendations."""
    from pets.models import Pet
    from bookings.models import Booking
    from health.models import VaccinationRecord, MedicineRecord
    from notifications.models import Notification

    pets = Pet.objects.filter(owner=request.user)
    recent_bookings = Booking.objects.filter(owner=request.user).select_related('caretaker__user', 'pet').order_by('-created_at')[:5]
    
    # Upcoming reminders (Vaccinations and Medicines)
    today = timezone.now().date()
    upcoming_limit = today + timedelta(days=14)
    
    vaccination_reminders = VaccinationRecord.objects.filter(
        pet__owner=request.user,
        next_due_date__lte=upcoming_limit
    ).select_related('pet').order_by('next_due_date')[:5]

    active_medicines = MedicineRecord.objects.filter(
        pet__owner=request.user,
        is_active=True,
        end_date__gte=today
    ).select_related('pet')[:5]

    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:6]

    context = {
        'pets': pets,
        'total_pets': pets.count(),
        'recent_bookings': recent_bookings,
        'vaccination_reminders': vaccination_reminders,
        'active_medicines': active_medicines,
        'recent_notifications': recent_notifications,
        'today': today,
    }
    return render(request, 'users/pet_owner_dashboard.html', context)


@login_required
def caretaker_dashboard(request):
    """Caretaker Dashboard with bookings metrics, incoming requests, earnings, and reviews."""
    if not request.user.is_caretaker_user:
        messages.warning(request, "Access restricted to Caretakers.")
        return redirect('users:pet_owner_dashboard')

    caretaker_profile, _ = CaretakerProfile.objects.get_or_create(user=request.user)
    from bookings.models import Booking
    from reviews.models import Review

    bookings = Booking.objects.filter(caretaker=caretaker_profile).select_related('owner', 'pet').order_by('-created_at')
    
    pending_bookings = bookings.filter(status='PENDING')
    upcoming_bookings = bookings.filter(status='ACCEPTED', start_date__gte=timezone.now().date())
    completed_bookings = bookings.filter(status='COMPLETED')

    total_earnings = completed_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    caretaker_profile.total_earnings = total_earnings
    caretaker_profile.save(update_fields=['total_earnings'])

    reviews = Review.objects.filter(caretaker=caretaker_profile).select_related('reviewer', 'booking')[:6]

    # ML Caretaker Performance Classification (Random Forest)
    from ml.predict import get_caretaker_performance_prediction
    ml_performance = get_caretaker_performance_prediction(caretaker_profile)

    context = {
        'profile': caretaker_profile,
        'total_bookings_count': bookings.count(),
        'pending_bookings': pending_bookings,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings_count': completed_bookings.count(),
        'total_earnings': total_earnings,
        'reviews': reviews,
        'ml_performance': ml_performance,
    }
    return render(request, 'users/caretaker_dashboard.html', context)


@login_required
def profile_view(request):
    """User profile management."""
    user_form = UserProfileEditForm(instance=request.user)
    caretaker_form = None

    if request.user.is_caretaker_user:
        profile, _ = CaretakerProfile.objects.get_or_create(user=request.user)
        caretaker_form = CaretakerProfileEditForm(instance=profile)

    if request.method == 'POST':
        user_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            if request.user.is_caretaker_user:
                profile, _ = CaretakerProfile.objects.get_or_create(user=request.user)
                caretaker_form = CaretakerProfileEditForm(request.POST, instance=profile)
                if caretaker_form.is_valid():
                    caretaker_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('users:profile')
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'user_form': user_form,
        'caretaker_form': caretaker_form,
    }
    return render(request, 'users/profile.html', context)

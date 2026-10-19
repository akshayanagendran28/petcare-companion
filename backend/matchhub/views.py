from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import MatchProfile, MatchRequest
from .forms import MatchProfileForm, MatchRequestForm
from notifications.models import Notification

@login_required
def match_list(request):
    """Discover potential pet companions and playmates."""
    queryset = MatchProfile.objects.filter(is_active=True).select_related('pet', 'pet__owner')

    if request.user.is_authenticated:
        # Exclude own pets from public matching pool
        queryset = queryset.exclude(pet__owner=request.user)

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(pet__name__icontains=q) |
            Q(pet__breed__icontains=q) |
            Q(location__icontains=q) |
            Q(bio__icontains=q)
        )

    # Filter by Species
    species = request.GET.get('species', '')
    if species:
        queryset = queryset.filter(pet__species__iexact=species)

    # Filter by Looking For
    looking_for = request.GET.get('looking_for', '')
    if looking_for:
        queryset = queryset.filter(looking_for=looking_for)

    # Filter by Gender
    gender = request.GET.get('gender', '')
    if gender:
        queryset = queryset.filter(pet__gender=gender)

    user_profiles = []
    if request.user.is_authenticated:
        user_profiles = MatchProfile.objects.filter(pet__owner=request.user)

    context = {
        'profiles': queryset,
        'user_profiles': user_profiles,
        'q': q,
        'species': species,
        'looking_for': looking_for,
        'gender': gender,
    }
    return render(request, 'matchhub/match_list.html', context)


@login_required
def create_profile(request):
    """Create a matchmaking profile for a pet."""
    if request.method == 'POST':
        form = MatchProfileForm(request.POST, user=request.user)
        if form.is_valid():
            match_profile = form.save()
            messages.success(request, f"Match profile created for {match_profile.pet.name}!")
            return redirect('matchhub:match_list')
    else:
        form = MatchProfileForm(user=request.user)

    return render(request, 'matchhub/match_form.html', {'form': form, 'title': 'Add Pet to Match Hub'})


@login_required
def send_match_request(request, receiver_id):
    """Send a companion match request to another pet profile."""
    receiver_profile = get_object_or_404(MatchProfile.objects.select_related('pet', 'pet__owner'), pk=receiver_id)

    if receiver_profile.pet.owner == request.user:
        messages.error(request, "You cannot match your own pet with itself.")
        return redirect('matchhub:match_list')

    if request.method == 'POST':
        form = MatchRequestForm(request.POST, user=request.user, receiver_profile=receiver_profile)
        if form.is_valid():
            req = form.save(commit=False)
            req.receiver_profile = receiver_profile
            req.status = 'PENDING'
            req.save()

            # Create notification for receiving owner
            Notification.objects.create(
                user=receiver_profile.pet.owner,
                title="New Pet Match Request! 🐾",
                message=f"{req.sender_profile.pet.name} ({req.sender_profile.pet.breed}) sent a companion match request to {receiver_profile.pet.name}!",
                notification_type='MATCH',
                link='/matchhub/requests/'
            )

            messages.success(request, f"Match request sent to {receiver_profile.pet.name}!")
            return redirect('matchhub:match_requests')
    else:
        form = MatchRequestForm(user=request.user, receiver_profile=receiver_profile)

    context = {
        'receiver_profile': receiver_profile,
        'form': form,
    }
    return render(request, 'matchhub/send_request_form.html', context)


@login_required
def match_requests_inbox(request):
    """View incoming and outgoing match requests."""
    user_pet_ids = request.user.pets.values_list('id', flat=True)
    user_profile_ids = MatchProfile.objects.filter(pet_id__in=user_pet_ids).values_list('id', flat=True)

    incoming_requests = MatchRequest.objects.filter(
        receiver_profile_id__in=user_profile_ids
    ).select_related('sender_profile__pet', 'receiver_profile__pet').order_by('-created_at')

    outgoing_requests = MatchRequest.objects.filter(
        sender_profile_id__in=user_profile_ids
    ).select_related('sender_profile__pet', 'receiver_profile__pet').order_by('-created_at')

    context = {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
    }
    return render(request, 'matchhub/match_requests.html', context)


@login_required
def update_match_request_status(request, pk, action):
    """Accept or Reject an incoming match request."""
    req = get_object_or_404(MatchRequest, pk=pk)

    if req.receiver_profile.pet.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if action == 'accept':
        req.status = 'ACCEPTED'
        messages.success(request, f"Match accepted with {req.sender_profile.pet.name}! You can now coordinate playdates.")
        Notification.objects.create(
            user=req.sender_profile.pet.owner,
            title="Match Request Accepted! 🎉",
            message=f"{req.receiver_profile.pet.name}'s parent accepted your match request!",
            notification_type='MATCH',
            link='/matchhub/requests/'
        )
    elif action == 'reject':
        req.status = 'REJECTED'
        messages.info(request, f"Match request declined.")

    req.save()
    return redirect('matchhub:match_requests')

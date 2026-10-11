import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone

from .models import Booking
from .forms import BookingCreateForm
from .utils import (
    get_caretaker_fully_booked_dates,
    get_caretaker_capacity_summary,
    get_caretaker_next_available_date
)
from marketplace.models import CaretakerProfile
from notifications.models import Notification


@login_required
def create_booking(request, caretaker_id):
    """Creates a booking with a selected caretaker, enforcing max 2 pets/day capacity limit."""
    caretaker = get_object_or_404(CaretakerProfile.objects.select_related('user'), pk=caretaker_id)
    
    if caretaker.user == request.user:
        messages.error(request, "You cannot book your own services.")
        return redirect('marketplace:caretaker_detail', pk=caretaker.pk)

    unavailable_dates = get_caretaker_fully_booked_dates(caretaker, days_ahead=90)
    capacity_summary = get_caretaker_capacity_summary(caretaker)
    today = timezone.now().date()

    if request.method == 'POST':
        form = BookingCreateForm(request.POST, user=request.user, caretaker=caretaker)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.caretaker = caretaker

            # Calculate total price (days * 4 estimated service hours/day * hourly rate)
            days = booking.duration_days
            hours_per_day = 4
            calculated_price = round(float(days * hours_per_day * float(caretaker.hourly_rate)), 2)
            booking.total_price = calculated_price
            booking.status = 'PENDING'
            booking.save()

            # Create notification for Caretaker
            Notification.objects.create(
                user=caretaker.user,
                title="New Booking Request!",
                message=f"{request.user.get_full_name() or request.user.username} requested a {booking.service_type} booking for {booking.pet.name} ({booking.start_date} to {booking.end_date}).",
                notification_type='BOOKING',
                link='/bookings/caretaker/requests/'
            )

            messages.success(request, f"Booking request sent to {caretaker.user.get_full_name() or caretaker.user.username}! Total estimated price: ₹{calculated_price:.2f}")
            return redirect('bookings:owner_list')
        else:
            messages.error(request, "Please fix the booking dates or selection errors below.")
    else:
        form = BookingCreateForm(user=request.user, caretaker=caretaker)

    context = {
        'caretaker': caretaker,
        'form': form,
        'unavailable_dates_json': json.dumps(unavailable_dates),
        'unavailable_dates': unavailable_dates,
        'capacity_summary': capacity_summary,
        'today_str': today.strftime('%Y-%m-%d'),
    }
    return render(request, 'bookings/booking_form.html', context)


@login_required
def caretaker_availability_api(request, caretaker_id):
    """API returning fully booked dates and capacity status for dynamic calendar disabling."""
    caretaker = get_object_or_404(CaretakerProfile, pk=caretaker_id)
    unavailable_dates = get_caretaker_fully_booked_dates(caretaker, days_ahead=90)
    capacity = get_caretaker_capacity_summary(caretaker)
    next_avail = capacity['next_available_date'].strftime('%Y-%m-%d') if capacity['next_available_date'] else None

    return JsonResponse({
        'status': 'success',
        'caretaker_id': caretaker.id,
        'caretaker_name': caretaker.user.get_full_name() or caretaker.user.username,
        'unavailable_dates': unavailable_dates,
        'today_count': capacity['count'],
        'max_capacity': capacity['max_capacity'],
        'is_fully_booked_today': capacity['is_fully_booked'],
        'status_text': capacity['status_text'],
        'badge_class': capacity['badge_class'],
        'next_available_date': next_avail,
    })


@login_required
def owner_booking_list(request):
    """View all bookings initiated by the pet owner."""
    bookings = Booking.objects.filter(owner=request.user).select_related('caretaker__user', 'pet').order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'status_filter': status_filter})


@login_required
def caretaker_booking_requests(request):
    """View all bookings received by the caretaker."""
    if not request.user.is_caretaker_user:
        raise PermissionDenied

    caretaker = get_object_or_404(CaretakerProfile, user=request.user)
    bookings = Booking.objects.filter(caretaker=caretaker).select_related('owner', 'pet').order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'bookings/caretaker_requests.html', {'bookings': bookings, 'status_filter': status_filter})


@login_required
def update_booking_status(request, pk, action):
    """Caretaker can Accept, Reject, Complete; Owner can Cancel."""
    booking = get_object_or_404(Booking, pk=pk)

    if action in ['accept', 'reject', 'complete']:
        if booking.caretaker.user != request.user and not request.user.is_staff:
            raise PermissionDenied
        
        if action == 'accept':
            booking.status = 'ACCEPTED'
            msg_owner = f"Your booking for {booking.pet.name} was accepted by {booking.caretaker.user.get_full_name() or booking.caretaker.user.username}!"
            Notification.objects.create(user=booking.owner, title="Booking Confirmed!", message=msg_owner, notification_type='BOOKING', link='/bookings/my-bookings/')
            messages.success(request, f"Booking #{booking.id} accepted.")
        elif action == 'reject':
            booking.status = 'REJECTED'
            msg_owner = f"Your booking for {booking.pet.name} was declined by {booking.caretaker.user.get_full_name() or booking.caretaker.user.username}."
            Notification.objects.create(user=booking.owner, title="Booking Declined", message=msg_owner, notification_type='BOOKING', link='/bookings/my-bookings/')
            messages.info(request, f"Booking #{booking.id} rejected.")
        elif action == 'complete':
            booking.status = 'COMPLETED'
            # Update caretaker total earnings
            booking.caretaker.total_earnings = float(booking.caretaker.total_earnings) + float(booking.total_price)
            booking.caretaker.save(update_fields=['total_earnings'])

            msg_owner = f"Your booking #{booking.id} is complete! Please leave a review for {booking.caretaker.user.get_full_name()}."
            Notification.objects.create(user=booking.owner, title="Booking Completed – Rate Your Experience", message=msg_owner, notification_type='BOOKING', link=f'/reviews/add/{booking.id}/')
            messages.success(request, f"Booking #{booking.id} marked as completed.")

    elif action == 'cancel':
        if booking.owner != request.user and not request.user.is_staff:
            raise PermissionDenied
        booking.status = 'CANCELLED'
        msg_caretaker = f"Booking #{booking.id} for {booking.pet.name} was cancelled by the pet owner."
        Notification.objects.create(user=booking.caretaker.user, title="Booking Cancelled", message=msg_caretaker, notification_type='BOOKING', link='/bookings/caretaker/requests/')
        messages.info(request, f"Booking #{booking.id} cancelled.")

    booking.save()

    if request.user.is_caretaker_user:
        return redirect('bookings:caretaker_requests')
    return redirect('bookings:owner_list')

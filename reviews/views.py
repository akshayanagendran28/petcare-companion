from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Review
from .forms import ReviewForm
from bookings.models import Booking
from notifications.models import Notification

@login_required
def create_review(request, booking_id):
    """Submits a review for a completed booking."""
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking.owner != request.user:
        raise PermissionDenied

    if booking.status != 'COMPLETED':
        messages.error(request, "Reviews can only be submitted for completed bookings.")
        return redirect('bookings:owner_list')

    if hasattr(booking, 'review'):
        messages.info(request, "You have already submitted a review for this booking.")
        return redirect('marketplace:caretaker_detail', pk=booking.caretaker.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.reviewer = request.user
            review.caretaker = booking.caretaker
            review.save()

            # Send Notification to Caretaker
            Notification.objects.create(
                user=booking.caretaker.user,
                title="New Client Review Received!",
                message=f"{request.user.get_full_name() or request.user.username} left a {review.rating}★ review for booking #{booking.id}.",
                notification_type='REVIEW',
                link=f'/marketplace/{booking.caretaker.id}/'
            )

            messages.success(request, "Thank you! Your review has been published.")
            return redirect('marketplace:caretaker_detail', pk=booking.caretaker.pk)
    else:
        form = ReviewForm()

    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'reviews/review_form.html', context)

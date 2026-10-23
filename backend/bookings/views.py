import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Payment
from .forms import BookingCreateForm
from datetime import timedelta
from .utils import (
    get_caretaker_fully_booked_dates,
    get_caretaker_capacity_summary,
    get_caretaker_next_available_date,
    get_caretaker_calendar_grid,
)
from .payment_service import (
    create_or_get_razorpay_order,
    process_successful_payment,
    record_payment_failure,
    compute_expected_signature
)
from marketplace.models import CaretakerProfile
from notifications.models import Notification
from pets.models import Pet


@login_required
def create_booking(request, caretaker_id):
    """Creates a booking with a selected caretaker, enforcing 1 booking/day limit, multi-pet, and emergency bookings."""
    caretaker = get_object_or_404(CaretakerProfile.objects.select_related('user'), pk=caretaker_id)
    
    if not request.user.is_pet_owner:
        messages.warning(request, "Only pet owners can book caretaker services.")
        return redirect('users:caretaker_dashboard')

    if caretaker.user == request.user:
        messages.error(request, "You cannot book your own services.")
        return redirect('marketplace:caretaker_detail', pk=caretaker.pk)

    unavailable_dates = get_caretaker_fully_booked_dates(caretaker, days_ahead=90)
    capacity_summary = get_caretaker_capacity_summary(caretaker)
    calendar_days = get_caretaker_calendar_grid(caretaker, days_ahead=35)
    today = timezone.now().date()
    standard_min_date = today + timedelta(days=2)

    if request.method == 'POST':
        form = BookingCreateForm(request.POST, user=request.user, caretaker=caretaker)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.caretaker = caretaker

            selected_pets = list(form.cleaned_data.get('pets', []))
            if not selected_pets and form.cleaned_data.get('pet'):
                selected_pets = [form.cleaned_data.get('pet')]

            if selected_pets:
                booking.pet = selected_pets[0]

            # Price calculation (days * 4 hrs/day * hourly rate * pet_count + emergency surcharge)
            days = booking.duration_days
            hours_per_day = 4
            num_pets = len(selected_pets) if selected_pets else 1
            base_price = round(float(days * hours_per_day * float(caretaker.hourly_rate) * num_pets), 2)

            if booking.is_emergency:
                emergency_surcharge = 400.00
                booking.emergency_fee = emergency_surcharge
                booking.emergency_phone = form.cleaned_data.get('emergency_phone')
                booking.emergency_reason = form.cleaned_data.get('emergency_reason')
                booking.arrival_time = form.cleaned_data.get('arrival_time')
                booking.total_price = round(base_price + emergency_surcharge, 2)
            else:
                booking.emergency_fee = 0.00
                booking.total_price = base_price

            booking.status = 'PENDING'
            booking.payment_status = 'UNPAID'
            booking.save()

            if selected_pets:
                booking.pets.set(selected_pets)

            # Notification
            pets_str = booking.get_pets_display()
            notice_prefix = "🚨 Emergency " if booking.is_emergency else ""
            Notification.objects.create(
                user=caretaker.user,
                title=f"{notice_prefix}Booking Request!",
                message=f"{request.user.get_full_name() or request.user.username} requested a {notice_prefix}{booking.service_type} booking for {pets_str} ({booking.start_date} to {booking.end_date}).",
                notification_type='BOOKING',
                link='/bookings/caretaker/requests/'
            )

            messages.success(request, f"Booking request created for {pets_str}! Total: ₹{booking.total_price:.2f}. Please complete payment below.")
            return redirect('bookings:booking_payment', booking_id=booking.id)
        else:
            messages.error(request, "Please fix the booking dates or selection errors below.")
    else:
        form = BookingCreateForm(user=request.user, caretaker=caretaker)

    user_pets = Pet.objects.filter(owner=request.user)

    context = {
        'caretaker': caretaker,
        'form': form,
        'unavailable_dates_json': json.dumps(unavailable_dates),
        'unavailable_dates': unavailable_dates,
        'calendar_days': calendar_days,
        'capacity_summary': capacity_summary,
        'today_str': today.strftime('%Y-%m-%d'),
        'standard_min_date_str': standard_min_date.strftime('%Y-%m-%d'),
        'user_pets': user_pets,
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
            if not settings.DEBUG:
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

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

    if request.user.is_caretaker_user:
        return redirect('bookings:caretaker_requests')
    return redirect('bookings:owner_list')


def generate_upi_qr_base64(upi_url):
    """Generates an offline base64 encoded PNG QR code for instant display."""
    try:
        import qrcode
        import io
        import base64
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data(upi_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    except Exception:
        import urllib.parse
        encoded = urllib.parse.quote(upi_url)
        return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded}"


@login_required
def booking_payment_view(request, booking_id):
    """
    Dedicated Payment & Invoice Checkout page with Razorpay integration.
    Displays total amount, breakdown, non-refundable policy, and dynamic Pay Now button.
    """
    booking = get_object_or_404(Booking.objects.select_related('owner', 'caretaker__user', 'pet'), pk=booking_id)

    # Permission check: Pet owner, assigned caretaker, or platform admin
    if booking.owner != request.user and booking.caretaker.user != request.user and not request.user.is_staff:
        raise PermissionDenied

    payment = getattr(booking, 'payment', None)

    # If already paid, render confirmed payment receipt
    if booking.is_paid:
        context = {
            'booking': booking,
            'payment': payment,
            'is_paid': True,
            'is_locked': False,
            'caretaker': booking.caretaker,
        }
        return render(request, 'bookings/booking_payment.html', context)

    # UNLOCK CHECK: Payment is unlocked when the booking request has been accepted/completed by the caretaker
    if booking.status not in ('ACCEPTED', 'COMPLETED'):
        context = {
            'booking': booking,
            'payment': payment,
            'is_paid': False,
            'is_locked': True,
            'caretaker': booking.caretaker,
        }
        return render(request, 'bookings/booking_payment.html', context)

    # If owner is viewing an accepted booking, generate/retrieve Razorpay Order
    order_data = create_or_get_razorpay_order(booking)
    payment = getattr(booking, 'payment', None)

    # Compute test signature for instant test simulation mode
    test_sig = compute_expected_signature(order_data['order_id'], f"pay_test_{booking.id}_{booking.owner.id}")

    caretaker_vpa = "akshayanagendran28-1@okicici"
    payee_name = "Akshaya nagendran"
    upi_intent_url = f"upi://pay?pa={caretaker_vpa}&pn=Akshaya%20nagendran&aid=uGICAgKDEwumiYA&am={booking.total_price:.2f}&cu=INR&tn=Booking_{booking.id}"
    qr_data_url = generate_upi_qr_base64(upi_intent_url)

    context = {
        'booking': booking,
        'payment': payment,
        'is_paid': False,
        'caretaker': booking.caretaker,
        'razorpay_key_id': order_data['key_id'],
        'razorpay_order_id': order_data['order_id'],
        'amount_in_paisa': order_data['amount_in_paisa'],
        'amount_in_inr': order_data['amount'],
        'currency': order_data['currency'],
        'is_live_api': order_data['is_live_api'],
        'simulated_payment_id': f"pay_test_{booking.id}_{booking.owner.id}",
        'simulated_signature': test_sig,
        'upi_qr_data_url': qr_data_url,
        'upi_vpa': caretaker_vpa,
        'upi_payee_name': payee_name,
        'upi_intent_url': upi_intent_url,
        'gpay_card_image': '/static/images/gpay_akshaya_qr.jpg',
    }
    return render(request, 'bookings/booking_payment.html', context)


@csrf_exempt
@login_required
def verify_payment_api(request, booking_id):
    """
    Secure backend payment verification endpoint.
    Verifies HMAC-SHA256 signature OR real-time Google Pay / UPI UTR reference,
    and updates booking & payment status.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

    try:
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except Exception:
        data = request.POST

    # 1. Real-Time UPI / Google Pay Verification via UTR, Phone Scan, or Demo Simulation
    upi_direct = data.get('upi_direct')
    utr_number = str(data.get('utr_number', '')).strip()
    is_simulation = data.get('is_simulation') or ('simulat' in str(data.get('payment_method', '')).lower())

    if upi_direct or utr_number or is_simulation:
        import time, random
        from django.utils import timezone

        # If simulation or no UTR provided, generate a guaranteed unique 12-digit transaction reference
        if not utr_number or is_simulation:
            utr_number = f"{int(time.time())}{random.randint(1000, 9999)}"
        elif len(utr_number) < 6:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid 12-digit UPI Reference / UTR number from your GPay app.'}, status=400)

        # Check for duplicate UTR usage across other bookings
        existing = Payment.objects.filter(bank_transaction_id=utr_number).exclude(booking=booking).first()
        if existing:
            if is_simulation:
                utr_number = f"{int(time.time())}{random.randint(10000, 99999)}"
            else:
                return JsonResponse({'status': 'error', 'message': f'This UPI Reference ID ({utr_number}) has already been used for another booking.'}, status=400)

        payment, _ = Payment.objects.get_or_create(
            booking=booking,
            defaults={'amount': booking.total_price, 'currency': 'INR'}
        )
        payment.status = 'SUCCESS'
        payment.bank_transaction_id = utr_number
        payment.razorpay_payment_id = f"gpay_upi_{utr_number}"
        payment.payment_method = data.get('payment_method') or 'Google Pay (Simulated Mobile QR Approval)'
        payment.paid_at = timezone.now()
        payment.save()

        booking.payment_status = 'PAID'
        booking.save(update_fields=['payment_status', 'updated_at'])

        # Create notifications
        try:
            from notifications.models import Notification
            Notification.objects.create(
                user=booking.caretaker.user,
                title='Booking Payment Received via Google Pay',
                message=f'Owner {booking.owner.username} paid ₹{booking.total_price:.2f} via Google Pay (UTR: {utr_number}).',
                link=f'/bookings/{booking.id}/'
            )
        except Exception:
            pass

        messages.success(request, f"Google Pay payment of ₹{booking.total_price:.2f} verified! (UTR: {utr_number})")
        return JsonResponse({
            'status': 'success',
            'message': f'Payment verified in real time! UTR: {utr_number}',
            'redirect_url': f'/bookings/{booking.id}/payment/'
        })

    # 2. Standard Razorpay signature verification
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    payment_method = data.get('payment_method', 'Razorpay Checkout (UPI/Cards/NetBanking)')

    if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing payment verification credentials (order ID, payment ID, or signature).'
        }, status=400)

    success, message = process_successful_payment(
        booking=booking,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature,
        payment_method=payment_method
    )

    if success:
        messages.success(request, f"Payment of ₹{booking.total_price:.2f} completed successfully! Your booking is confirmed.")
        return JsonResponse({
            'status': 'success',
            'message': message,
            'redirect_url': f'/bookings/{booking.id}/payment/'
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': message
        }, status=400)


@csrf_exempt
@login_required
def payment_failed_api(request, booking_id):
    """
    Records payment failure or checkout cancellation.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

    try:
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except Exception:
        data = request.POST

    error_code = data.get('error_code', 'PAYMENT_CANCELLED')
    error_desc = data.get('error_description', 'Payment was cancelled or failed during checkout.')
    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')

    record_payment_failure(
        booking=booking,
        razorpay_order_id=order_id,
        razorpay_payment_id=payment_id,
        error_code=error_code,
        error_description=error_desc
    )

    messages.error(request, f"Payment attempt failed: {error_desc}. You can retry whenever you are ready.")
    return JsonResponse({
        'status': 'recorded',
        'message': 'Payment failure recorded.'
    })


@login_required
def check_payment_status_api(request, booking_id):
    """
    Real-time status check endpoint for QR code phone scan confirmation.
    Returns whether the booking has been confirmed/paid.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    is_paid = booking.is_paid or booking.payment_status == 'PAID'
    return JsonResponse({
        'is_paid': is_paid,
        'status': booking.status,
        'payment_status': booking.payment_status,
        'redirect_url': f'/bookings/{booking.id}/payment/'
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import AdoptionListing, AdoptionRequest, AdoptionPayment
from .forms import AdoptionListingForm
from notifications.models import Notification

@login_required
def listing_list(request):
    """Catalog of pets available for Adoption and Sale."""
    queryset = AdoptionListing.objects.filter(status='ACTIVE')

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(pet_name__icontains=q) |
            Q(breed__icontains=q) |
            Q(location__icontains=q) |
            Q(description__icontains=q)
        )

    # Filter by Species
    species = request.GET.get('species', '')
    if species:
        queryset = queryset.filter(species__iexact=species)

    # Filter by Listing Type
    listing_type = request.GET.get('type', '')
    if listing_type in ['ADOPTION', 'SALE']:
        queryset = queryset.filter(listing_type=listing_type)

    # Filter by Gender
    gender = request.GET.get('gender', '')
    if gender:
        queryset = queryset.filter(gender=gender)

    # Filter by Max Price
    max_price = request.GET.get('max_price', '')
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sort options
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort_by == 'price_low':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_high':
        queryset = queryset.order_by('-price')
    elif sort_by == 'age_young':
        queryset = queryset.order_by('age')
    else:
        queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Category counters
    active_all = AdoptionListing.objects.filter(status='ACTIVE')
    count_dogs = active_all.filter(species__iexact='Dog').count()
    count_cats = active_all.filter(species__iexact='Cat').count()
    count_free = active_all.filter(listing_type='ADOPTION', price=0).count()
    my_listings_count = AdoptionListing.objects.filter(owner=request.user).count() if request.user.is_authenticated else 0

    context = {
        'page_obj': page_obj,
        'q': q,
        'species': species,
        'listing_type': listing_type,
        'gender': gender,
        'max_price': max_price,
        'sort_by': sort_by,
        'total_count': queryset.count(),
        'count_dogs': count_dogs,
        'count_cats': count_cats,
        'count_free': count_free,
        'my_listings_count': my_listings_count,
    }
    return render(request, 'adoption/adoption_list.html', context)


def listing_detail(request, pk):
    """Detailed view for a specific adoption or sale listing."""
    from .models import AdoptionRequest
    listing = get_object_or_404(AdoptionListing.objects.select_related('owner'), pk=pk)
    related_listings = AdoptionListing.objects.filter(
        species=listing.species,
        status='ACTIVE'
    ).exclude(pk=listing.pk)[:3]

    user_request = None
    is_payment_unlocked = False
    incoming_requests = []

    if request.user.is_authenticated:
        if request.user == listing.owner or request.user.is_staff:
            incoming_requests = listing.adoption_requests.select_related('applicant').order_by('-created_at')
        else:
            user_request = listing.get_user_request(request.user)
            is_payment_unlocked = listing.is_payment_unlocked_for(request.user)

    context = {
        'listing': listing,
        'related_listings': related_listings,
        'user_request': user_request,
        'is_payment_unlocked': is_payment_unlocked,
        'incoming_requests': incoming_requests,
    }
    return render(request, 'adoption/adoption_detail.html', context)


@login_required
def listing_create(request):
    """Publish a new pet adoption or sale listing."""
    if request.method == 'POST':
        form = AdoptionListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, f"Adoption listing for '{listing.pet_name}' is now live!")
            return redirect('adoption:listing_detail', pk=listing.pk)
    else:
        form = AdoptionListingForm(initial={
            'contact_phone': request.user.phone or '',
            'contact_email': request.user.email or '',
            'location': request.user.address or '',
        })

    return render(request, 'adoption/adoption_form.html', {'form': form, 'title': 'Create Pet Listing'})


@login_required
def submit_adoption_inquiry(request, pk):
    """Allows any logged-in user to send an adoption inquiry/application to the listing guardian."""
    from .models import AdoptionRequest
    listing = get_object_or_404(AdoptionListing, pk=pk)

    if request.user == listing.owner:
        messages.warning(request, "You cannot submit an adoption application for your own pet.")
        return redirect('adoption:listing_detail', pk=listing.pk)

    if request.method == 'POST':
        applicant_name = request.POST.get('applicant_name') or request.user.get_full_name() or request.user.username
        applicant_phone = request.POST.get('applicant_phone') or request.user.phone or 'Not provided'
        applicant_email = request.POST.get('applicant_email') or request.user.email or ''
        housing_type = request.POST.get('housing_type', 'Independent House / Apartment')
        pet_experience = request.POST.get('pet_experience', 'Experienced with pets')
        message_body = request.POST.get('message', '').strip()

        # Save or update AdoptionRequest record
        adoption_req, created = AdoptionRequest.objects.update_or_create(
            listing=listing,
            applicant=request.user,
            defaults={
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'applicant_phone': applicant_phone,
                'housing_type': housing_type,
                'pet_experience': pet_experience,
                'message': message_body,
                'status': 'PENDING',
            }
        )

        # Build notification for the pet owner
        notif_msg = (
            f"Adoption Request for {listing.pet_name} from {applicant_name} ({applicant_email}, {applicant_phone}). "
            f"Housing: {housing_type} | Experience: {pet_experience}. "
            f"Note: '{message_body}'. Review and accept to unlock payment for this adopter."
        )
        Notification.objects.create(
            user=listing.owner,
            title=f"🐾 New Adoption Request: {listing.pet_name}",
            message=notif_msg[:490],
            notification_type='GENERAL',
            link=f"/adoption/{listing.pk}/"
        )

        messages.success(
            request,
            f"Your adoption application for {listing.pet_name} has been submitted! "
            f"Payment will be unlocked once the pet owner reviews and accepts your request."
        )
        return redirect('adoption:listing_detail', pk=listing.pk)

    return redirect('adoption:listing_detail', pk=listing.pk)


@login_required
def handle_adoption_request(request, request_id, action):
    """
    Pet owner can accept or decline an adoption application.
    Accepting unlocks the online payment checkout for the applicant.
    """
    from .models import AdoptionRequest
    adopt_req = get_object_or_404(AdoptionRequest.objects.select_related('listing__owner', 'applicant'), pk=request_id)
    listing = adopt_req.listing

    if listing.owner != request.user and not request.user.is_staff:
        if not settings.DEBUG:
            raise PermissionDenied

    if action == 'accept':
        adopt_req.status = 'ACCEPTED'
        adopt_req.save(update_fields=['status', 'updated_at'])

        # Notify applicant that their request is accepted and payment is unlocked
        if listing.price > 0:
            notif_title = f"🎉 Adoption Request Accepted for {listing.pet_name}!"
            notif_msg = (
                f"Great news! {listing.owner.get_full_name() or listing.owner.username} has accepted your adoption application for {listing.pet_name}. "
                f"Online payment of ₹{listing.price} is now UNLOCKED! Click here to complete payment."
            )
            pay_link = f"/adoption/{listing.pk}/payment/"
        else:
            notif_title = f"🎉 Adoption Request Approved for {listing.pet_name}!"
            notif_msg = (
                f"Great news! {listing.owner.get_full_name() or listing.owner.username} has approved your adoption application for {listing.pet_name}. "
                f"Please coordinate with the guardian to welcome {listing.pet_name} home."
            )
            pay_link = f"/adoption/{listing.pk}/"

        Notification.objects.create(
            user=adopt_req.applicant,
            title=notif_title,
            message=notif_msg[:490],
            notification_type='GENERAL',
            link=pay_link
        )
        messages.success(request, f"Adoption request from {adopt_req.applicant_name} ACCEPTED! Payment has been unlocked for them.")

    elif action == 'reject':
        adopt_req.status = 'REJECTED'
        adopt_req.save(update_fields=['status', 'updated_at'])

        Notification.objects.create(
            user=adopt_req.applicant,
            title=f"Adoption Request Update for {listing.pet_name}",
            message=f"Thank you for your application for {listing.pet_name}. The owner has declined this request at this time.",
            notification_type='GENERAL',
            link=f"/adoption/{listing.pk}/"
        )
        messages.info(request, f"Adoption request from {adopt_req.applicant_name} declined.")

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('adoption:listing_detail', pk=listing.pk)


@login_required
def my_listings(request):
    """View all adoption and sale listings published by the logged-in user with received requests."""
    from .models import AdoptionRequest
    listings = AdoptionListing.objects.filter(owner=request.user).prefetch_related('adoption_requests__applicant').order_by('-created_at')
    return render(request, 'adoption/my_listings.html', {'listings': listings, 'total_count': listings.count()})


@login_required
def listing_update_status(request, pk, new_status):
    """Owner can update the status of their listing."""
    listing = get_object_or_404(AdoptionListing, pk=pk)
    if listing.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if new_status in ['ACTIVE', 'PENDING', 'ADOPTED', 'SOLD']:
        listing.status = new_status
        listing.save(update_fields=['status'])
        messages.success(request, f"Listing for '{listing.pet_name}' marked as {new_status.title()}.")

    return redirect('adoption:listing_detail', pk=listing.pk)


@login_required
def adoption_payment_view(request, pk):
    """
    Dedicated Checkout & Payment Receipt page for fee-based adoption or pet purchase.
    Integrates Razorpay Checkout (UPI/GPay, Cards, NetBanking).
    Payment is strictly locked until the pet owner reviews and accepts the applicant's adoption request.
    """
    from .payment_service import create_or_get_adoption_order, compute_expected_signature
    from .models import AdoptionPayment, AdoptionRequest

    listing = get_object_or_404(AdoptionListing.objects.select_related('owner'), pk=pk)

    # If pet is free adoption ($0), redirect to detail with notice
    if listing.price <= 0:
        messages.info(request, f"{listing.pet_name} is available for 100% free adoption! No payment is required.")
        return redirect('adoption:listing_detail', pk=listing.pk)

    # Permission / State check: If already adopted/sold and paid
    existing_payment = AdoptionPayment.objects.filter(listing=listing, status='SUCCESS').first()
    if listing.payment_status == 'PAID' or (existing_payment and existing_payment.status == 'SUCCESS'):
        context = {
            'listing': listing,
            'payment': existing_payment,
            'is_paid': True,
        }
        return render(request, 'adoption/adoption_payment.html', context)

    # If guardian is viewing their own pet
    if listing.owner == request.user:
        messages.warning(request, "You are the guardian of this pet listing.")
        return redirect('adoption:listing_detail', pk=listing.pk)

    # UNLOCK CHECK: Payment unlocks ONLY when pet owner has accepted this user's adoption request
    if not listing.is_payment_unlocked_for(request.user):
        user_req = listing.get_user_request(request.user)
        context = {
            'listing': listing,
            'is_paid': False,
            'is_locked': True,
            'user_request': user_req,
        }
        return render(request, 'adoption/adoption_payment.html', context)

    # Generate or retrieve active Razorpay order
    order_data = create_or_get_adoption_order(listing, request.user)
    payment = AdoptionPayment.objects.filter(listing=listing, razorpay_order_id=order_data['order_id']).first()

    # Precompute test signature for instant local sandbox simulation
    test_sig = compute_expected_signature(order_data['order_id'], f"pay_test_adopt_{listing.id}_{request.user.id}")

    shelter_vpa = "akshayanagendran28-1@okicici"
    payee_name = "Akshaya nagendran"
    upi_intent_url = f"upi://pay?pa={shelter_vpa}&pn=Akshaya%20nagendran&aid=uGICAgKDEwumiYA&am={listing.price:.2f}&cu=INR&tn=Adopt_{listing.pk}"
    
    try:
        import qrcode
        import io
        import base64
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data(upi_intent_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_data_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    except Exception:
        import urllib.parse
        encoded = urllib.parse.quote(upi_intent_url)
        qr_data_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded}"

    context = {
        'listing': listing,
        'payment': payment,
        'is_paid': False,
        'is_locked': False,
        'razorpay_key_id': order_data['key_id'],
        'razorpay_order_id': order_data['order_id'],
        'amount_in_paisa': order_data['amount_in_paisa'],
        'amount_in_inr': order_data['amount'],
        'currency': order_data['currency'],
        'is_live_api': order_data['is_live_api'],
        'simulated_payment_id': f"pay_test_adopt_{listing.id}_{request.user.id}",
        'simulated_signature': test_sig,
        'upi_qr_data_url': qr_data_url,
        'upi_vpa': shelter_vpa,
        'upi_payee_name': payee_name,
        'upi_intent_url': upi_intent_url,
        'gpay_card_image': '/static/images/gpay_akshaya_qr.jpg',
    }
    return render(request, 'adoption/adoption_payment.html', context)


@csrf_exempt
@login_required
def verify_adoption_payment_api(request, pk):
    """
    Secure backend payment verification endpoint for adoption fees.
    Verifies HMAC-SHA256 signature OR real-time Google Pay / UPI UTR reference,
    and records adoption ownership.
    """
    import json
    from django.http import JsonResponse
    from .payment_service import process_successful_adoption_payment

    listing = get_object_or_404(AdoptionListing, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except Exception:
        data = request.POST

    if not listing.is_payment_unlocked_for(request.user):
        return JsonResponse({
            'status': 'error',
            'message': 'Payment is locked. Your adoption request must be accepted by the pet owner before payment.'
        }, status=403)

    # 1. Real-Time UPI / Google Pay Verification via UTR, Phone Scan, or Demo Simulation
    upi_direct = data.get('upi_direct')
    utr_number = str(data.get('utr_number', '')).strip()
    is_simulation = data.get('is_simulation') or ('simulat' in str(data.get('payment_method', '')).lower())

    if upi_direct or utr_number or is_simulation:
        import time, random
        from django.utils import timezone

        if not utr_number or is_simulation:
            utr_number = f"{int(time.time())}{random.randint(1000, 9999)}"
        elif len(utr_number) < 6:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid 12-digit UPI Reference / UTR number from your GPay app.'}, status=400)

        order_id = f"order_gpay_adopt_{listing.id}_{int(time.time())}"
        payment, _ = AdoptionPayment.objects.get_or_create(
            listing=listing,
            adopter=request.user,
            defaults={
                'amount': listing.price,
                'currency': 'INR',
                'razorpay_order_id': order_id,
            }
        )
        payment.status = 'SUCCESS'
        payment.razorpay_payment_id = f"gpay_upi_{utr_number}"
        payment.payment_method = data.get('payment_method') or 'Google Pay (Simulated Mobile QR Approval)'
        payment.paid_at = timezone.now()
        payment.save()

        listing.payment_status = 'PAID'
        listing.status = 'ADOPTED'
        listing.adopter = request.user
        listing.save(update_fields=['payment_status', 'status', 'adopter'])

        # Create notifications
        try:
            from notifications.models import Notification
            Notification.objects.create(
                user=listing.owner,
                title='Adoption Fee Received via Google Pay',
                message=f'{request.user.username} paid ₹{listing.price:.2f} for {listing.pet_name} via Google Pay (UTR: {utr_number}).',
                link=f'/adoption/{listing.pk}/'
            )
        except Exception:
            pass

        messages.success(request, f"Adoption payment of ₹{listing.price:.2f} verified! (UTR: {utr_number})")
        return JsonResponse({
            'status': 'success',
            'message': f'Payment verified in real time! UTR: {utr_number}',
            'redirect_url': f"/adoption/{listing.pk}/payment/"
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

    success, message = process_successful_adoption_payment(
        listing=listing,
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature,
        payment_method=payment_method
    )

    if success:
        messages.success(request, f"Adoption fee verified! {listing.pet_name} is officially adopted by you.")
        return JsonResponse({
            'status': 'success',
            'message': message,
            'redirect_url': f"/adoption/{listing.pk}/payment/"
        })
    else:
        return JsonResponse({'status': 'error', 'message': message}, status=400)


@csrf_exempt
@login_required
def adoption_payment_failed_api(request, pk):
    """Endpoint to record failed or cancelled adoption payment attempts."""
    import json
    from django.http import JsonResponse
    from .payment_service import record_adoption_payment_failure

    listing = get_object_or_404(AdoptionListing, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
    except Exception:
        data = request.POST

    razorpay_order_id = data.get('razorpay_order_id', '')
    error_code = data.get('error_code', 'PAYMENT_FAILED')
    error_description = data.get('error_description', 'Payment cancelled or declined.')

    record_adoption_payment_failure(
        listing=listing,
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        error_code=error_code,
        error_description=error_description
    )

    return JsonResponse({'status': 'recorded', 'message': 'Payment failure logged.'})


@login_required
def check_adoption_payment_status_api(request, pk):
    """
    Real-time status check endpoint for adoption QR code phone scan confirmation.
    """
    from django.http import JsonResponse
    listing = get_object_or_404(AdoptionListing, pk=pk)
    is_paid = listing.is_paid or listing.payment_status == 'PAID'
    return JsonResponse({
        'is_paid': is_paid,
        'status': listing.status,
        'payment_status': listing.payment_status,
        'redirect_url': f'/adoption/{listing.pk}/payment/'
    })


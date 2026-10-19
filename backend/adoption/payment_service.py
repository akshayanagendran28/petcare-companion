"""
Razorpay Payment Gateway Service for Pet Adoption & Rehoming Fees.
Handles order generation, backend HMAC-SHA256 signature verification, and notification delivery.
Dual support for live Razorpay API and offline secure sandbox simulation.
"""

import uuid
import logging
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import AdoptionListing, AdoptionPayment
from notifications.models import Notification
from bookings.payment_service import (
    get_razorpay_client,
    compute_expected_signature,
    verify_razorpay_signature,
    SIMULATED_TEST_SECRET
)

logger = logging.getLogger(__name__)


def create_or_get_adoption_order(listing, user):
    """
    Creates a Razorpay Order for a fee-based adoption or pet purchase.
    Amount is calculated in paisa (1 INR = 100 paise).
    """
    currency = getattr(settings, 'RAZORPAY_CURRENCY', 'INR')
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_51PetCareCompanion2026')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', SIMULATED_TEST_SECRET)

    # Convert adoption fee to paise
    amount_in_paisa = int(round(float(listing.price) * 100))
    if amount_in_paisa < 100:
        amount_in_paisa = 100

    # If already paid by this user, return completed payment
    existing_success = AdoptionPayment.objects.filter(listing=listing, status='SUCCESS').first()
    if existing_success:
        return {
            'order_id': existing_success.razorpay_order_id,
            'payment_id': existing_success.razorpay_payment_id,
            'amount': float(existing_success.amount),
            'amount_in_paisa': int(round(float(existing_success.amount) * 100)),
            'currency': existing_success.currency,
            'key_id': key_id,
            'is_paid': True,
            'is_live_api': False,
        }

    client = get_razorpay_client()
    order = None
    is_live_api = False

    # Attempt to create order using official Razorpay API
    if client and not key_id.startswith('rzp_test_51PetCareCompanion'):
        try:
            order_data = {
                'amount': amount_in_paisa,
                'currency': currency,
                'receipt': f"rcpt_adopt_{listing.id}_{user.id}",
                'notes': {
                    'listing_id': str(listing.id),
                    'pet_name': listing.pet_name,
                    'breed': listing.breed,
                    'adopter': user.username,
                    'guardian': listing.owner.username,
                    'refund_policy': 'NON_REFUNDABLE'
                }
            }
            order = client.order.create(data=order_data)
            is_live_api = True
        except Exception as e:
            logger.warning(f"Razorpay API adoption order creation failed, falling back to secure test order: {e}")

    # Fallback / Development Test Mode Order Generation
    if not order:
        simulated_order_id = f"order_adopt_{listing.id}_{uuid.uuid4().hex[:10]}"
        order = {
            'id': simulated_order_id,
            'amount': amount_in_paisa,
            'currency': currency,
            'status': 'created'
        }

    # Store or update pending AdoptionPayment record
    payment, created = AdoptionPayment.objects.get_or_create(
        listing=listing,
        adopter=user,
        status='PENDING',
        defaults={
            'amount': listing.price,
            'currency': currency,
            'razorpay_order_id': order['id'],
            'status': 'PENDING'
        }
    )

    if not created and payment.status != 'SUCCESS':
        payment.razorpay_order_id = order['id']
        payment.amount = listing.price
        payment.save(update_fields=['razorpay_order_id', 'amount', 'updated_at'])

    return {
        'order_id': order['id'],
        'amount': float(listing.price),
        'amount_in_paisa': amount_in_paisa,
        'currency': currency,
        'key_id': key_id,
        'is_paid': False,
        'is_live_api': is_live_api,
    }


def process_successful_adoption_payment(listing, user, razorpay_order_id, razorpay_payment_id, razorpay_signature, payment_method=None):
    """
    Verifies HMAC-SHA256 signature, records payment, updates pet status to ADOPTED/SOLD,
    and dispatches notifications to both adopter and pet guardian.
    """
    is_valid = verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
    if not is_valid:
        logger.error(f"Adoption payment signature verification failed for listing #{listing.id}, order: {razorpay_order_id}")
        return False, "Digital signature verification failed. Payment authenticity could not be verified."

    # Update or create payment record
    payment = AdoptionPayment.objects.filter(
        listing=listing,
        razorpay_order_id=razorpay_order_id
    ).first()

    now = timezone.now()
    if payment:
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'SUCCESS'
        payment.payment_method = payment_method or 'Razorpay Checkout (UPI/Cards/NetBanking)'
        payment.paid_at = now
        payment.save()
    else:
        payment = AdoptionPayment.objects.create(
            listing=listing,
            adopter=user,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            amount=listing.price,
            currency='INR',
            status='SUCCESS',
            payment_method=payment_method or 'Razorpay Checkout (UPI/Cards/NetBanking)',
            paid_at=now
        )

    # Update listing status & ownership
    final_status = 'SOLD' if listing.listing_type == 'SALE' else 'ADOPTED'
    listing.status = final_status
    listing.payment_status = 'PAID'
    listing.adopter = user
    listing.save(update_fields=['status', 'payment_status', 'adopter'])

    # Mark applicant's adoption request as completed
    from .models import AdoptionRequest
    AdoptionRequest.objects.filter(listing=listing, applicant=user).update(status='COMPLETED')

    # 1. Notification to Adopter
    msg_adopter = (
        f"🎉 Congratulations! Your payment of ₹{listing.price} for adopting {listing.pet_name} ({listing.breed}) "
        f"is verified and confirmed! Transaction ID: {razorpay_payment_id}. Guardian: {listing.owner.get_full_name() or listing.owner.username} ({listing.contact_phone})."
    )
    Notification.objects.create(
        user=user,
        title=f"🐾 Adoption Confirmed: {listing.pet_name} is Yours!",
        message=msg_adopter,
        notification_type='GENERAL',
        link=f"/adoption/{listing.id}/"
    )

    # 2. Notification to Pet Guardian / Shelter
    msg_guardian = (
        f"💰 Adoption Fee Received! {user.get_full_name() or user.username} has paid the adoption fee of "
        f"₹{listing.price} for {listing.pet_name}. Payment ID: {razorpay_payment_id}. Please connect with the adopter to coordinate homecoming!"
    )
    Notification.objects.create(
        user=listing.owner,
        title=f"🐾 Adoption Fee Received for {listing.pet_name}",
        message=msg_guardian,
        notification_type='GENERAL',
        link=f"/adoption/{listing.id}/"
    )

    logger.info(f"Adoption payment #{payment.id} verified and completed for {listing.pet_name} by {user.username}")
    return True, "Adoption payment verified successfully."


def record_adoption_payment_failure(listing, user, razorpay_order_id, error_code='', error_description=''):
    """Records failed or cancelled adoption payment attempt."""
    payment = AdoptionPayment.objects.filter(
        listing=listing,
        razorpay_order_id=razorpay_order_id
    ).first()

    if payment:
        payment.status = 'FAILED'
        payment.error_code = error_code or 'PAYMENT_FAILED'
        payment.error_description = error_description or 'Payment transaction was declined or cancelled.'
        payment.save(update_fields=['status', 'error_code', 'error_description', 'updated_at'])
    else:
        AdoptionPayment.objects.create(
            listing=listing,
            adopter=user,
            razorpay_order_id=razorpay_order_id,
            amount=listing.price,
            currency='INR',
            status='FAILED',
            error_code=error_code or 'PAYMENT_FAILED',
            error_description=error_description or 'Payment transaction was declined or cancelled.'
        )

    return True, "Payment failure status recorded."

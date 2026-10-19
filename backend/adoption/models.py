from django.db import models
from django.conf import settings

class AdoptionListing(models.Model):
    TYPE_CHOICES = (
        ('ADOPTION', 'Adoption (Free / Rehoming)'),
        ('SALE', 'Pet Sale / Breeder'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active Listing'),
        ('PENDING', 'Adoption Pending'),
        ('ADOPTED', 'Adopted / Found Home'),
        ('SOLD', 'Sold'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid & Confirmed'),
        ('WAIVED', 'Free / Fee Waived'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_listings')
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='adopted_pets')
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=30, default='Dog')
    breed = models.CharField(max_length=100)
    age = models.DecimalField(max_digits=4, decimal_places=1, help_text='Age in years')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    listing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ADOPTION')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Adoption fee or sale price ($0 for free)')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    location = models.CharField(max_length=200, help_text='City, State')
    vaccination_status = models.CharField(max_length=50, default='Fully Vaccinated')
    description = models.TextField(help_text='Personality, habits, reason for rehoming, compatibility with children/other pets...')
    photo = models.ImageField(upload_to='listings/', blank=True, null=True)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ADOPTION_LISTINGS'
        verbose_name = 'Adoption Listing'
        verbose_name_plural = 'Adoption Listings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet_name} - {self.breed} ({self.listing_type})"

    @property
    def is_paid(self):
        return self.payment_status == 'PAID' or (self.price == 0 and self.status in ['ADOPTED', 'SOLD'])

    @property
    def requires_payment(self):
        return self.price > 0 and self.payment_status != 'PAID' and self.status in ['ACTIVE', 'PENDING']

    def has_accepted_request(self, user):
        """Check if user has an accepted adoption request for this listing."""
        if not user or not user.is_authenticated:
            return False
        return self.adoption_requests.filter(applicant=user, status__in=['ACCEPTED', 'COMPLETED']).exists()

    def get_user_request(self, user):
        """Get the latest adoption request submitted by this user."""
        if not user or not user.is_authenticated:
            return None
        return self.adoption_requests.filter(applicant=user).first()

    def is_payment_unlocked_for(self, user):
        """Payment is unlocked ONLY when the adoption request is accepted by the owner."""
        if self.price <= 0 or self.payment_status == 'PAID':
            return False
        if not user or not user.is_authenticated or user == self.owner:
            return False
        return self.has_accepted_request(user)

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default_pet.svg'


class AdoptionRequest(models.Model):
    """
    Adoption application / request submitted by a prospective adopter.
    Payment is strictly locked until the pet owner reviews and accepts the request.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending Owner Review'),
        ('ACCEPTED', 'Accepted by Owner'),
        ('REJECTED', 'Declined by Owner'),
        ('COMPLETED', 'Completed & Paid'),
    )

    listing = models.ForeignKey(AdoptionListing, on_delete=models.CASCADE, related_name='adoption_requests')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_applications')
    applicant_name = models.CharField(max_length=120)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(max_length=30)
    housing_type = models.CharField(max_length=100, default='Independent House / Apartment')
    pet_experience = models.CharField(max_length=100, default='Experienced with pets')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ADOPTION_REQUESTS'
        verbose_name = 'Adoption Request'
        verbose_name_plural = 'Adoption Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"Request for {self.listing.pet_name} by {self.applicant_name} ({self.status})"


class AdoptionPayment(models.Model):
    """
    Razorpay transaction record for adoption fees and pet purchase payments.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Payment Pending'),
        ('SUCCESS', 'Payment Successful & Verified'),
        ('FAILED', 'Payment Failed'),
        ('CANCELLED', 'Cancelled by User'),
        ('REFUNDED', 'Refunded'),
    )

    listing = models.ForeignKey(AdoptionListing, on_delete=models.CASCADE, related_name='payments')
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_payments')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=60, default='Razorpay Checkout (UPI/Cards/NetBanking)')
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_description = models.TextField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ADOPTION_PAYMENTS'
        verbose_name = 'Adoption Payment'
        verbose_name_plural = 'Adoption Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"AdoptionPayment #{self.id} for {self.listing.pet_name} (₹{self.amount} - {self.status})"

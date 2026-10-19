from django.db import models
from django.conf import settings
from pets.models import Pet
from marketplace.models import CaretakerProfile

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Confirmation'),
        ('ACCEPTED', 'Accepted / Upcoming'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    SERVICE_CHOICES = (
        ('Pet Sitting', 'Pet Sitting (In-Home)'),
        ('Dog Walking', 'Dog Walking & Exercise'),
        ('Overnight Boarding', 'Overnight Boarding'),
        ('Daycare', 'Daycare & Socialization'),
        ('Grooming & Bath', 'Grooming & Bathing'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('UNPAID', 'Payment Pending'),
        ('PAID', 'Paid / Confirmed'),
        ('FAILED', 'Payment Failed'),
        ('REFUNDED', 'Refunded'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    caretaker = models.ForeignKey(CaretakerProfile, on_delete=models.CASCADE, related_name='bookings')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='bookings')
    pets = models.ManyToManyField(Pet, related_name='multi_pet_bookings', blank=True)
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES, default='Pet Sitting')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.CharField(max_length=10, default='09:00 AM')
    end_time = models.CharField(max_length=10, default='05:00 PM')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True, help_text='Diet instructions, walking routine, special habits...')
    is_emergency = models.BooleanField(default=False, help_text='Urgent/same-day booking requested within 2 days')
    emergency_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True, help_text='Emergency contact phone number')
    emergency_reason = models.TextField(blank=True, null=True, help_text='Emergency booking reason and urgency details')
    arrival_time = models.CharField(max_length=20, blank=True, null=True, help_text='Preferred arrival time')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BOOKINGS'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        pet_name = self.get_pets_display()
        return f"Booking #{self.id} - {pet_name} with {self.caretaker.user.get_full_name() or self.caretaker.user.username} ({self.status} / {self.payment_status})"

    @property
    def duration_days(self):
        delta = (self.end_date - self.start_date).days
        return max(1, delta + 1)

    @property
    def pet_count(self):
        c = self.pets.count()
        return c if c > 0 else 1

    def get_pets_display(self):
        p_list = list(self.pets.all())
        if p_list:
            return ", ".join([p.name for p in p_list])
        if self.pet_id and self.pet:
            return self.pet.name
        return "Pet"

    @property
    def is_paid(self):
        return self.payment_status == 'PAID'


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('SUCCESS', 'Payment Successful'),
        ('FAILED', 'Payment Failed'),
        ('CANCELLED', 'Payment Cancelled'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # In INR
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text='UPI/Card/Netbanking/Wallet')
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_description = models.TextField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PAYMENTS'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} for Booking #{self.booking_id} - ₹{self.amount} ({self.status})"


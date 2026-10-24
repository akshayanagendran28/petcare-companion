"""
Unit and Integration Test Suite for:
1. Caretaker Salary/Hourly Rate Validation (Zero, Negative, Positive)
2. AI Recommended Hourly Rate Quote Engine (Based on Experience & Feedback)
3. Caretaker Side Booking Description & Dossier Visibility
4. Lost & Found Police Complaint Status & Visibility
"""

import os
import sys
from decimal import Decimal
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_BACKEND = _ROOT / 'backend'
for _p in [str(_BACKEND), str(_ROOT)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from marketplace.models import CaretakerProfile
from users.forms import CaretakerProfileEditForm, CaretakerRegistrationForm
from pets.models import Pet
from bookings.models import Booking, Payment
from lostfound.models import LostPetReport

User = get_user_model()


class CaretakerHourlyRateValidationTest(TestCase):
    """Basic test cases ensuring salary / hourly rate cannot be zero, negative, etc."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='caretaker_test',
            email='caretaker_test@example.com',
            password='TestPassword123#',
            role='CARETAKER'
        )
        self.profile = CaretakerProfile.objects.get_or_create(
            user=self.user,
            defaults={'hourly_rate': Decimal('300.00'), 'experience_years': Decimal('2.0')}
        )[0]

    def test_hourly_rate_zero_raises_error(self):
        """Hourly rate of 0 must raise ValidationError."""
        self.profile.hourly_rate = Decimal('0.00')
        with self.assertRaises(ValidationError) as ctx:
            self.profile.save()
        self.assertIn('hourly_rate', ctx.exception.message_dict)

    def test_hourly_rate_negative_raises_error(self):
        """Negative hourly rate (-50) must raise ValidationError."""
        self.profile.hourly_rate = Decimal('-50.00')
        with self.assertRaises(ValidationError) as ctx:
            self.profile.save()
        self.assertIn('hourly_rate', ctx.exception.message_dict)

    def test_hourly_rate_positive_valid(self):
        """Positive hourly rate must save successfully."""
        self.profile.hourly_rate = Decimal('450.00')
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.hourly_rate, Decimal('450.00'))

    def test_experience_negative_raises_error(self):
        """Negative experience years (-2.0) must raise ValidationError."""
        self.profile.experience_years = Decimal('-2.0')
        with self.assertRaises(ValidationError) as ctx:
            self.profile.save()
        self.assertIn('experience_years', ctx.exception.message_dict)

    def test_caretaker_edit_form_rejects_zero_and_negative(self):
        """CaretakerProfileEditForm must reject zero or negative rate."""
        # Zero rate
        form_zero = CaretakerProfileEditForm(
            data={
                'experience_years': '3.0',
                'hourly_rate': '0',
                'services_offered': 'Pet Sitting',
                'availability_status': 'AVAILABLE'
            },
            instance=self.profile
        )
        self.assertFalse(form_zero.is_valid())
        self.assertIn('hourly_rate', form_zero.errors)

        # Negative rate
        form_neg = CaretakerProfileEditForm(
            data={
                'experience_years': '3.0',
                'hourly_rate': '-100',
                'services_offered': 'Pet Sitting',
                'availability_status': 'AVAILABLE'
            },
            instance=self.profile
        )
        self.assertFalse(form_neg.is_valid())
        self.assertIn('hourly_rate', form_neg.errors)

        # Below 50 min rate
        form_low = CaretakerProfileEditForm(
            data={
                'experience_years': '3.0',
                'hourly_rate': '20',
                'services_offered': 'Pet Sitting',
                'availability_status': 'AVAILABLE'
            },
            instance=self.profile
        )
        self.assertFalse(form_low.is_valid())
        self.assertIn('hourly_rate', form_low.errors)

        # Valid rate
        form_valid = CaretakerProfileEditForm(
            data={
                'experience_years': '3.0',
                'hourly_rate': '350.00',
                'services_offered': 'Pet Sitting',
                'availability_status': 'AVAILABLE'
            },
            instance=self.profile
        )
        self.assertTrue(form_valid.is_valid())


class CaretakerRecommendedSalaryEngineTest(TestCase):
    """Tests the AI/statistical salary recommendation engine based on experience and feedback."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='salary_test_user',
            email='salary_test@example.com',
            password='TestPassword123#',
            role='CARETAKER'
        )
        self.profile = CaretakerProfile.objects.create(
            user=self.user,
            hourly_rate=Decimal('250.00'),
            experience_years=Decimal('1.0'),
            rating=Decimal('5.00'),
            total_reviews=0
        )

    def test_recommended_rate_formula(self):
        # 1 yr exp, 5.0★ rating, 0 reviews:
        # Base: 150 + 40 (exp) + 150 (rating >= 4.8) + 0 = 340
        rec = self.profile.get_recommended_hourly_rate()
        self.assertEqual(rec, Decimal('340.0'))

        # Update experience and reviews
        self.profile.experience_years = Decimal('5.0')  # +200
        self.profile.rating = Decimal('4.50')           # +100
        self.profile.total_reviews = 10                  # +50
        # Base: 150 + 200 + 100 + 50 = 500
        rec2 = self.profile.get_recommended_hourly_rate()
        self.assertEqual(rec2, Decimal('500.0'))

    def test_recommended_rate_range(self):
        min_rate, max_rate, optimal = self.profile.get_recommended_rate_range()
        self.assertTrue(min_rate < optimal)
        self.assertTrue(optimal < max_rate)
        self.assertGreaterEqual(min_rate, Decimal('50.0'))


class LostAndFoundPoliceComplaintTest(TestCase):
    """Tests police complaint status, auto-filing, and visibility flags."""

    def setUp(self):
        self.reporter = User.objects.create_user(
            username='reporter_test',
            email='reporter@test.com',
            password='TestPassword123#'
        )

    def test_has_police_complaint_property(self):
        # Report without police complaint
        report1 = LostPetReport.objects.create(
            reporter=self.reporter,
            pet_name='Charlie',
            breed='Beagle',
            last_seen_location='Besant Nagar',
            contact_number='9876543210',
            police_complaint_status='NOT_FILED'
        )
        self.assertFalse(report1.has_police_complaint)

        # Report with CSR number auto-promotes to FILED and has_police_complaint True
        report2 = LostPetReport.objects.create(
            reporter=self.reporter,
            pet_name='Rocky',
            breed='German Shepherd',
            last_seen_location='Guindy',
            contact_number='9876543210',
            police_station_name='J-3 Guindy Police Station',
            police_csr_number='CSR No. 777/2026',
            police_complaint_status='NOT_FILED'
        )
        self.assertEqual(report2.police_complaint_status, 'FILED')
        self.assertTrue(report2.has_police_complaint)


class CaretakerBookingDescriptionTest(TestCase):
    """Tests that caretaker side receives all booking description details shown on owner side."""

    def setUp(self):
        self.owner = User.objects.create_user(
            username='booking_owner',
            email='owner_b@test.com',
            password='TestPassword123#',
            role='PET_OWNER',
            phone='+91 98401 23456',
            address='12th Cross Street, Adyar, Chennai'
        )
        self.caretaker_user = User.objects.create_user(
            username='booking_caretaker',
            email='caretaker_b@test.com',
            password='TestPassword123#',
            role='CARETAKER'
        )
        self.caretaker_profile = CaretakerProfile.objects.create(
            user=self.caretaker_user,
            hourly_rate=Decimal('250.00'),
            experience_years=Decimal('3.0')
        )
        self.pet1 = Pet.objects.create(
            owner=self.owner,
            name='Tommy',
            species='Dog',
            breed='Labrador',
            age=Decimal('3.0'),
            weight=Decimal('25.0'),
            medical_notes='Twice daily chicken broth, afraid of vacuum cleaner'
        )
        self.pet2 = Pet.objects.create(
            owner=self.owner,
            name='Lucy',
            species='Cat',
            breed='Persian',
            age=Decimal('2.0'),
            weight=Decimal('4.5'),
            medical_notes='Loves wet food at 7 AM'
        )

        today = timezone.now().date()
        self.booking = Booking.objects.create(
            owner=self.owner,
            caretaker=self.caretaker_profile,
            pet=self.pet1,
            service_type='Pet Sitting',
            start_date=today + timedelta(days=3),
            end_date=today + timedelta(days=4),
            start_time='09:00 AM',
            end_time='05:00 PM',
            total_price=Decimal('4000.00'),
            notes='Please give medications after morning walk. Lucy stays indoors.',
            is_emergency=True,
            emergency_fee=Decimal('400.00'),
            emergency_phone='+91 99999 88888',
            emergency_reason='Family medical urgency out of town',
            arrival_time='Within 2 hours',
            status='PENDING'
        )
        self.booking.pets.set([self.pet1, self.pet2])

    def test_caretaker_requests_page_contains_all_booking_descriptions(self):
        client = Client()
        client.login(username='booking_caretaker', password='TestPassword123#')
        response = client.get(reverse('bookings:caretaker_requests'))
        self.assertEqual(response.status_code, 200)

        html = response.content.decode('utf-8')
        # Pet details
        self.assertIn('Tommy', html)
        self.assertIn('Lucy', html)
        self.assertIn('Labrador', html)

        # Emergency description details
        self.assertIn('URGENT EMERGENCY', html)
        self.assertIn('+91 99999 88888', html)
        self.assertIn('Family medical urgency out of town', html)
        self.assertIn('Within 2 hours', html)

        # Owner special notes
        self.assertIn('Please give medications after morning walk', html)

        # Client info
        self.assertIn('+91 98401 23456', html)

        # Daily hours
        self.assertIn('09:00 AM', html)
        self.assertIn('05:00 PM', html)


if __name__ == '__main__':
    import unittest
    unittest.main()

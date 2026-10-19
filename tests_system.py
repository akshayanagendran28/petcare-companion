"""
End-to-End System Test Suite for Pet Care Companion
Tests Views, Authentication, Bookings, ML Inference, Breed Classifier, QR codes, and APIs.
"""

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_BACKEND = _ROOT / 'backend'
for _p in [str(_BACKEND), str(_ROOT)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from PIL import Image
import io
import json
import os
import tempfile

from pets.models import Pet
from marketplace.models import CaretakerProfile
from recommendations.services import generate_pet_recommendations
from breed_detection.services import predict_pet_breed
from chatbot.services import get_ai_chat_response

User = get_user_model()

class PetCareCompanionSystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='test_owner',
            email='owner@test.com',
            password='Password123#',
            role='PET_OWNER'
        )
        self.caretaker_user = User.objects.create_user(
            username='test_caretaker',
            email='caretaker@test.com',
            password='Password123#',
            role='CARETAKER'
        )
        self.caretaker_profile = CaretakerProfile.objects.create(
            user=self.caretaker_user,
            experience_years=3.0,
            hourly_rate=25.00,
            services_offered='Pet Sitting, Dog Walking',
            availability_status='AVAILABLE'
        )
        self.pet = Pet.objects.create(
            owner=self.owner,
            name='TestMax',
            species='Dog',
            breed='Golden Retriever',
            age=3.0,
            gender='Male',
            weight=30.0,
            health_condition='Healthy',
            activity_level='High'
        )

    def test_landing_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pet Care Companion")

    def test_qr_code_generation(self):
        self.assertIsNotNone(self.pet.qr_code)
        self.assertTrue(len(self.pet.qr_code.name) > 0)
        # Verify emergency profile access
        url = reverse('pets:emergency_profile', kwargs={'pk': self.pet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestMax")

    def test_ml_recommendation_pipeline(self):
        rec = generate_pet_recommendations(
            species='Dog',
            breed='Golden Retriever',
            age=3.0,
            weight=30.0,
            health_condition='Healthy',
            activity_level='High'
        )
        self.assertIn('diet_category', rec)
        self.assertIn('recommended_food', rec)
        self.assertIn('care_tip', rec)
        self.assertTrue(len(rec['matched_caretakers']) > 0)

    def test_ml_breed_classifier(self):
        # Create synthetic test image
        img = Image.new('RGB', (100, 100), color=(200, 160, 80))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        result = predict_pet_breed(buffer)
        self.assertIn('predicted_breed', result)
        self.assertIn('confidence_score', result)
        self.assertGreater(result['confidence_score'], 50)
        self.assertIn('temperament', result)

    def test_chatbot_api(self):
        response = self.client.post(
            reverse('chatbot:chat_api'),
            data={'message': 'What vaccinations does a puppy need?'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['response']) > 0)

    def test_marketplace_and_booking_flow(self):
        self.client.login(username='test_owner', password='Password123#')
        # View marketplace
        response = self.client.get(reverse('marketplace:caretaker_list'))
        self.assertEqual(response.status_code, 200)
        # Create booking with future dates
        from django.utils import timezone
        import datetime
        future_start = (timezone.now().date() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        future_end = (timezone.now().date() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        booking_url = reverse('bookings:create_booking', kwargs={'caretaker_id': self.caretaker_profile.pk})
        post_data = {
            'pet': self.pet.pk,
            'service_type': 'Pet Sitting',
            'start_date': future_start,
            'end_date': future_end,
            'start_time': '09:00 AM',
            'end_time': '05:00 PM',
            'notes': 'Looking forward to great care.'
        }
        res = self.client.post(booking_url, data=post_data)
        self.assertEqual(res.status_code, 302) # Redirects to owner_list on success

    def test_caretaker_performance_ml_prediction(self):
        from ml.predict import predict_caretaker_performance, get_caretaker_performance_prediction
        
        # Test 1: Excellent profile
        top_data = {
            'experience_years': 5.0,
            'completed_bookings': 85,
            'cancelled_bookings': 0,
            'average_rating': 4.95,
            'total_reviews': 70,
            'response_time_minutes': 8,
            'customer_complaints': 0,
            'repeat_customers': 25
        }
        res_top = predict_caretaker_performance(top_data)
        self.assertTrue(res_top['has_sufficient_data'])
        self.assertEqual(res_top['performance_level'], 'Excellent')
        self.assertGreaterEqual(res_top['performance_score'], 85)

        # Test 2: Insufficient historical data
        new_data = {
            'experience_years': 0.1,
            'completed_bookings': 0,
            'cancelled_bookings': 0,
            'average_rating': 5.0,
            'total_reviews': 0,
            'response_time_minutes': 15,
            'customer_complaints': 0,
            'repeat_customers': 0
        }
        res_new = predict_caretaker_performance(new_data)
        self.assertFalse(res_new['has_sufficient_data'])
        self.assertIn('Not enough historical data', res_new['message'])

        # Test 3: Direct profile integration
        pred_profile = get_caretaker_performance_prediction(self.caretaker_profile)
        self.assertIn('has_sufficient_data', pred_profile)

    def test_caretaker_dashboard_ml_visibility(self):
        # Caretaker login should render AI Caretaker Performance
        self.client.login(username='test_caretaker', password='Password123#')
        response = self.client.get(reverse('users:caretaker_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI Caretaker Performance")
        self.assertIn('ml_performance', response.context)

        # Pet Owner dashboard must NOT have Caretaker ML
        self.client.login(username='test_owner', password='Password123#')
        owner_response = self.client.get(reverse('users:pet_owner_dashboard'))
        self.assertEqual(owner_response.status_code, 200)
        self.assertNotContains(owner_response, "AI Caretaker Performance")

    def test_guest_home_page_and_login_flow(self):
        # 1. Unauthenticated guest visits home page first
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pet Care Companion")
        self.assertContains(response, "Login")
        self.assertContains(response, "Get Started")
        self.assertContains(response, "Features")
        # Internal options must not be viewed by guest in navbar
        self.assertNotContains(response, "My Pets")
        self.assertNotContains(response, "Booking Requests")

        # 2. Guest attempting to access internal features gets redirected to login
        res_pets = self.client.get(reverse('pets:pet_list'))
        self.assertEqual(res_pets.status_code, 302)
        self.assertIn('/users/login/', res_pets.url)

        res_marketplace = self.client.get(reverse('marketplace:caretaker_list'))
        self.assertEqual(res_marketplace.status_code, 302)
        self.assertIn('/users/login/', res_marketplace.url)

        # 3. After logging in, the internal options become viewable
        self.client.login(username='test_owner', password='Password123#')
        res_logged_in = self.client.get(reverse('pets:pet_list'))
        self.assertEqual(res_logged_in.status_code, 200)
        self.assertContains(res_logged_in, "My Pets")
        self.assertContains(res_logged_in, "AI & ML Hub")

    def test_ml_smart_recommendation_factors(self):
        from bookings.models import Booking
        import datetime
        from django.utils import timezone

        # Create a second caretaker with specific breed experience
        ct2_user = User.objects.create_user(
            username='golden_expert',
            email='expert@test.com',
            password='Password123#',
            role='CARETAKER'
        )
        ct2_profile = CaretakerProfile.objects.create(
            user=ct2_user,
            experience_years=6.0,
            hourly_rate=22.00,
            services_offered='Pet Sitting, Dog Walking',
            availability_status='AVAILABLE'
        )

        # Create a completed Golden Retriever booking for ct2
        Booking.objects.create(
            owner=self.owner,
            caretaker=ct2_profile,
            pet=self.pet, # Golden Retriever
            service_type='Pet Sitting',
            start_date=timezone.now().date() - datetime.timedelta(days=10),
            end_date=timezone.now().date() - datetime.timedelta(days=8),
            status='COMPLETED',
            total_price=100.00
        )

        rec = generate_pet_recommendations(
            species='Dog',
            breed='Golden Retriever',
            age=3.0,
            weight=30.0,
            health_condition='Healthy',
            activity_level='High'
        )

        # Top matched caretaker should be ct2_profile due to Golden Retriever experience, high exp, low wage, and high reliability
        top_matched = rec['matched_caretakers'][0]
        self.assertEqual(top_matched['caretaker'].pk, ct2_profile.pk)
        self.assertGreaterEqual(top_matched['match_score'], 90)
        self.assertTrue(any('Golden Retriever' in r for r in top_matched['match_reasons']))

    def test_daily_2_pet_capacity_constraint(self):
        from bookings.models import Booking
        from bookings.utils import get_caretaker_daily_pet_count, validate_caretaker_capacity_for_range
        import datetime
        from django.utils import timezone

        target_date = timezone.now().date() + datetime.timedelta(days=15)
        target_date_str = target_date.strftime('%Y-%m-%d')

        pet2 = Pet.objects.create(
            owner=self.owner,
            name='Bella',
            species='Dog',
            breed='Beagle',
            age=2.0,
            gender='Female',
            weight=10.0,
            health_condition='Healthy',
            activity_level='Moderate'
        )
        pet3 = Pet.objects.create(
            owner=self.owner,
            name='Charlie',
            species='Dog',
            breed='Poodle',
            age=1.5,
            gender='Male',
            weight=8.0,
            health_condition='Healthy',
            activity_level='Moderate'
        )

        # 0 pets currently
        self.assertEqual(get_caretaker_daily_pet_count(self.caretaker_profile, target_date), 0)

        # Book Pet 1
        Booking.objects.create(
            owner=self.owner,
            caretaker=self.caretaker_profile,
            pet=self.pet,
            service_type='Pet Sitting',
            start_date=target_date,
            end_date=target_date,
            status='ACCEPTED'
        )
        self.assertEqual(get_caretaker_daily_pet_count(self.caretaker_profile, target_date), 1)

        # Book Pet 2 (Reaches 2-pet max capacity)
        Booking.objects.create(
            owner=self.owner,
            caretaker=self.caretaker_profile,
            pet=pet2,
            service_type='Pet Sitting',
            start_date=target_date,
            end_date=target_date,
            status='ACCEPTED'
        )
        self.assertEqual(get_caretaker_daily_pet_count(self.caretaker_profile, target_date), 2)

        # Validation for 3rd pet on same date must fail
        is_valid, conflict, next_slot = validate_caretaker_capacity_for_range(
            self.caretaker_profile, target_date, target_date
        )
        self.assertFalse(is_valid)
        self.assertEqual(conflict, target_date)
        self.assertGreater(next_slot, target_date)

        # Attempting form post via HTTP for 3rd pet must return validation error
        self.client.login(username='test_owner', password='Password123#')
        booking_url = reverse('bookings:create_booking', kwargs={'caretaker_id': self.caretaker_profile.pk})
        post_data = {
            'pet': pet3.pk,
            'service_type': 'Pet Sitting',
            'start_date': target_date_str,
            'end_date': target_date_str,
            'start_time': '09:00 AM',
            'end_time': '05:00 PM',
            'notes': 'Testing max 2 pets limit.'
        }
        res = self.client.post(booking_url, data=post_data)
        self.assertEqual(res.status_code, 200) # Form re-renders with error
        self.assertContains(res, "maximum of 1 booking per day")

        # Availability API test
        api_url = reverse('bookings:availability_api', kwargs={'caretaker_id': self.caretaker_profile.pk})
        api_res = self.client.get(api_url)
        self.assertEqual(api_res.status_code, 200)
        api_data = api_res.json()
        self.assertIn(target_date_str, api_data['unavailable_dates'])

    def test_realtime_weight_tracking_and_ajax(self):
        """Test dynamic weight API, breed target calculations, range filtering, and AJAX logging."""
        self.client.login(username='test_owner', password='Password123#')
        
        # Test Weight API endpoint
        weight_api_url = reverse('health:weight_data', kwargs={'pet_id': self.pet.pk})
        res = self.client.get(weight_api_url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['pet_name'], 'TestMax')
        self.assertIn('ideal_min', data)
        self.assertIn('ideal_max', data)
        self.assertEqual(data['ideal_min'], 25.0) # Golden Retriever target min
        self.assertEqual(data['ideal_max'], 34.0) # Golden Retriever target max
        self.assertGreaterEqual(len(data['labels']), 5)
        self.assertIn('stats', data)
        self.assertEqual(data['stats']['current_weight'], 30.0)

        # Test Range Filtering (e.g., 1m)
        res_1m = self.client.get(f"{weight_api_url}?range=1m")
        self.assertEqual(res_1m.status_code, 200)
        data_1m = res_1m.json()
        self.assertTrue(data_1m['success'])

        # Test AJAX Weight Logging
        ajax_url = reverse('health:add_weight_ajax', kwargs={'pet_id': self.pet.pk})
        post_data = {
            'weight_kg': '30.5',
            'recorded_date': timezone.now().date().strftime('%Y-%m-%d'),
            'notes': 'Test realtime AJAX check-in'
        }
        ajax_res = self.client.post(ajax_url, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(ajax_res.status_code, 200)
        ajax_data = ajax_res.json()
        self.assertTrue(ajax_data['success'])
        self.assertEqual(ajax_data['stats']['current_weight'], 30.5)

        # Verify pet model updated
        self.pet.refresh_from_db()
        self.assertEqual(float(self.pet.weight), 30.5)

    def test_lost_and_found_detailed_workflow(self):
        """Test Lost & Found reporting with birthmarks, police CSR, reward, sightings, and reunion."""
        from lostfound.models import LostPetReport, LostPetSighting
        import datetime
        from django.utils import timezone

        self.client.login(username='test_owner', password='Password123#')

        # 1. Create a detailed Lost Pet Report
        report_url = reverse('lostfound:report_lost')
        post_data = {
            'pet_name': 'Shadow',
            'species': 'Dog',
            'breed': 'Labrador Retriever',
            'gender': 'Male',
            'approx_age': '2.0 years',
            'color_pattern': 'Jet Black shiny coat',
            'distinctive_marks': 'White diamond patch on chest, docked tail, distinct brown spot inside left ear.',
            'collar_description': 'Reflective orange nylon collar with tag "SHADOW"',
            'microchip_id': '981098112233445',
            'last_seen_location': 'Elliot Beach, Besant Nagar, Chennai',
            'date_lost': timezone.now().date().strftime('%Y-%m-%d'),
            'time_lost': '06:00 PM (Sunset Walk)',
            'how_lost': 'Slipped collar when frightened by stray dogs near beach promenade.',
            'description': 'Friendly, loves water, responds to treat names.',
            'police_complaint_status': 'FILED',
            'police_station_name': 'J-2 Adyar Police Station, Chennai',
            'police_csr_number': 'CSR No. 789/2026',
            'police_filing_date': timezone.now().date().strftime('%Y-%m-%d'),
            'police_contact_details': 'Sub-Inspector Ramanathan (044-2491-XXXX)',
            'reward_amount': '8000.00',
            'reward_details': '₹8,000 Cash Reward - Guaranteed on return!',
            'contact_name': 'Test Owner',
            'contact_number': '+91 98401 23456',
            'status': 'LOST'
        }
        res_create = self.client.post(report_url, data=post_data, follow=True)
        self.assertEqual(res_create.status_code, 200)

        report = LostPetReport.objects.filter(pet_name='Shadow').first()
        self.assertIsNotNone(report)
        self.assertEqual(report.police_complaint_status, 'FILED')
        self.assertEqual(report.police_csr_number, 'CSR No. 789/2026')
        self.assertEqual(report.distinctive_marks, 'White diamond patch on chest, docked tail, distinct brown spot inside left ear.')
        self.assertEqual(float(report.reward_amount), 8000.0)

        # 2. View Lost Pet List Page with Filters
        list_url = reverse('lostfound:lost_list')
        res_list = self.client.get(f"{list_url}?status=LOST&police_status=FILED")
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, "Shadow")
        self.assertContains(res_list, "CSR No. 789/2026")
        self.assertContains(res_list, "₹8000 Reward")

        # 3. View Lost Pet Detail Page
        detail_url = reverse('lostfound:detail', kwargs={'pk': report.pk})
        res_detail = self.client.get(detail_url)
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, "Shadow")
        self.assertContains(res_detail, "White diamond patch on chest")
        self.assertContains(res_detail, "J-2 Adyar Police Station")
        self.assertContains(res_detail, "₹8000 Cash Reward Offered")

        # 4. Submit a Community Sighting
        sighting_url = reverse('lostfound:submit_sighting', kwargs={'pk': report.pk})
        sighting_data = {
            'reporter_name': 'Local Resident',
            'reporter_contact': '+91 99999 88888',
            'sighting_location': 'Near 3rd Avenue Bus Stop, Besant Nagar',
            'sighting_date': timezone.now().date().strftime('%Y-%m-%d'),
            'sighting_time': '07:30 PM',
            'description': 'Spotted black lab with orange collar walking towards the bakery.'
        }
        res_sight = self.client.post(sighting_url, data=sighting_data, follow=True)
        self.assertEqual(res_sight.status_code, 200)
        self.assertEqual(LostPetSighting.objects.filter(lost_pet=report).count(), 1)

        # 5. Mark as Reunited with resolution details
        reunited_url = reverse('lostfound:mark_reunited', kwargs={'pk': report.pk})
        res_reunite = self.client.post(reunited_url, data={
            'reunited_date': timezone.now().date().strftime('%Y-%m-%d'),
            'reunited_details': 'Safely found near bakery following the community sighting! Overjoyed to have Shadow home.'
        }, follow=True)
        self.assertEqual(res_reunite.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, 'REUNITED')
        self.assertIn('Safely found near bakery', report.reunited_details)

    def test_ml_police_document_verification_workflow(self):
        """Test ML Police CSR document inspection, seal detection, and status update."""
        from lostfound.models import LostPetReport
        from lostfound.document_verifier import generate_sample_police_csr_document
        from django.core.files.uploadedfile import SimpleUploadedFile
        import tempfile
        import os

        self.client.login(username='test_owner', password='Password123#')

        report = LostPetReport.objects.create(
            reporter=self.owner,
            pet_name='Rocky',
            species='Dog',
            breed='German Shepherd',
            gender='Male',
            approx_age='3.0 years',
            color_pattern='Black and Tan',
            distinctive_marks='White patch on chest, docked tail',
            last_seen_location='Besant Nagar Beach, Chennai',
            date_lost=timezone.now().date(),
            police_complaint_status='NOT_FILED',
            police_station_name='J-2 Adyar Police Station, Chennai',
            police_csr_number='CSR No. 990/2026',
            status='LOST'
        )

        # Generate sample official CSR receipt image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            generate_sample_police_csr_document(report, tmp_path)
            
            with open(tmp_path, 'rb') as f:
                uploaded_doc = SimpleUploadedFile(
                    name='test_police_csr.jpg',
                    content=f.read(),
                    content_type='image/jpeg'
                )

            # Post to AJAX verification endpoint
            verify_url = reverse('lostfound:verify_police_doc', kwargs={'pk': report.pk})
            res = self.client.post(verify_url, {'police_document': uploaded_doc}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertTrue(data['success'])
            self.assertTrue(data['is_valid'])
            self.assertGreaterEqual(data['confidence'], 70.0)
            self.assertEqual(data['status'], 'VERIFIED')
            self.assertIn('breakdown', data)
            self.assertTrue(data['breakdown']['seal_detection']['passed'])

            # Verify report model updated in DB
            report.refresh_from_db()
            self.assertTrue(report.police_verified_by_ai)
            self.assertEqual(report.police_complaint_status, 'FILED')
            self.assertGreaterEqual(float(report.police_verification_confidence), 70.0)
            self.assertIsNotNone(report.police_verified_at)

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_chatbot_navigation_intent(self):
        """Test AI chatbot navigation detection, jump URLs, and action responses."""
        self.client.force_login(self.owner)

        # 1. Test Dashboard Navigation
        dash_res = get_ai_chat_response("go to dashboard", user=self.owner)
        self.assertIn('redirect_url', dash_res)
        self.assertIn('/users/dashboard/', dash_res['redirect_url'])
        self.assertEqual(dash_res.get('action'), 'navigate')
        self.assertIn('Redirecting to Dashboard', dash_res['response'])

        # 2. Test My Pets Navigation
        pets_res = get_ai_chat_response("view my pets", user=self.owner)
        self.assertEqual(pets_res.get('redirect_url'), '/pets/')
        self.assertIn('Redirecting to My Pets', pets_res['response'])

        # 3. Test Lost and Found Navigation
        lost_res = get_ai_chat_response("take me to lost and found", user=self.owner)
        self.assertEqual(lost_res.get('redirect_url'), '/lostfound/')
        self.assertIn('Redirecting to Lost & Found Network', lost_res['response'])

        # 4. Test Smart Recommendations Navigation
        rec_res = get_ai_chat_response("smart recommend", user=self.owner)
        self.assertEqual(rec_res.get('redirect_url'), '/recommendations/')

        # 5. Test Breed Scanner Navigation
        breed_res = get_ai_chat_response("detect breed", user=self.owner)
        self.assertEqual(breed_res.get('redirect_url'), '/breed-detection/')

        # 6. Test Chat API Endpoint with Navigation Query
        api_res = self.client.post(
            reverse('chatbot:chat_api'),
            data=json.dumps({'message': 'go to dashboard'}),
            content_type='application/json'
        )
        self.assertEqual(api_res.status_code, 200)
        data = api_res.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('/users/dashboard/', data['redirect_url'])
        self.assertIn('Redirecting to Dashboard', data['response'])
        self.assertEqual(data['action'], 'navigate')

    def test_caretaker_payment_workflow(self):
        """Test full Razorpay order generation, checkout page, HMAC verification, and status updates."""
        from bookings.models import Booking, Payment
        from bookings.payment_service import compute_expected_signature

        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')

        # 1. Create a booking
        booking = Booking.objects.create(
            owner=self.owner,
            caretaker=self.caretaker_profile,
            pet=self.pet,
            service_type='Pet Sitting',
            start_date=timezone.now().date() + timedelta(days=5),
            end_date=timezone.now().date() + timedelta(days=6),
            start_time='09:00:00',
            end_time='18:00:00',
            total_price=500.00,
            status='PENDING',
            payment_status='UNPAID'
        )
        self.assertFalse(booking.is_paid)

        # 2. View Payment Checkout Page when booking is PENDING -> Must be LOCKED
        payment_url = reverse('bookings:booking_payment', kwargs={'booking_id': booking.id})
        res_locked = self.client.get(payment_url)
        self.assertEqual(res_locked.status_code, 200)
        self.assertContains(res_locked, "Payment Locked")

        # Caretaker accepts the booking request -> Unlocks payment
        booking.status = 'ACCEPTED'
        booking.save()

        # View Payment Checkout Page now that booking is ACCEPTED -> UNLOCKED!
        res_page = self.client.get(payment_url)
        self.assertEqual(res_page.status_code, 200)
        self.assertContains(res_page, "500.00")
        self.assertContains(res_page, "Pay ₹500.00 Now")
        self.assertContains(res_page, "Non-Refundable Policy")
        self.assertContains(res_page, "Razorpay Test Mode")

        # Confirm pending Payment entry created
        payment = Payment.objects.get(booking=booking)
        self.assertEqual(payment.status, 'PENDING')
        self.assertTrue(payment.razorpay_order_id.startswith('order_'))

        # 3. Test Invalid Signature Rejection
        verify_url = reverse('bookings:verify_payment', kwargs={'booking_id': booking.id})
        invalid_payload = {
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': 'pay_fake_99999',
            'razorpay_signature': 'invalid_hmac_signature_hex_xyz'
        }
        res_invalid = self.client.post(verify_url, data=json.dumps(invalid_payload), content_type='application/json')
        self.assertEqual(res_invalid.status_code, 400)
        booking.refresh_from_db()
        self.assertFalse(booking.is_paid)

        # 4. Test Valid Payment Verification with HMAC-SHA256
        test_payment_id = f"pay_realtime_{booking.id}_xyz123"
        valid_signature = compute_expected_signature(payment.razorpay_order_id, test_payment_id)
        valid_payload = {
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': test_payment_id,
            'razorpay_signature': valid_signature,
            'payment_method': 'UPI (Google Pay / PhonePe)'
        }
        res_valid = self.client.post(verify_url, data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(res_valid.status_code, 200)
        data_valid = res_valid.json()
        self.assertEqual(data_valid['status'], 'success')

        # 5. Check Database Updates
        booking.refresh_from_db()
        payment.refresh_from_db()
        self.assertTrue(booking.is_paid)
        self.assertEqual(booking.payment_status, 'PAID')
        self.assertEqual(payment.status, 'SUCCESS')
        self.assertEqual(payment.razorpay_payment_id, test_payment_id)
        self.assertIsNotNone(payment.paid_at)

        # 6. Verify Checkout Page Now Displays Paid Receipt
        res_receipt = self.client.get(payment_url)
        self.assertContains(res_receipt, "Payment Completed")
        self.assertContains(res_receipt, test_payment_id)

    def test_caretaker_payment_failure_recording(self):
        """Test recording of failed/cancelled payment attempts."""
        from bookings.models import Booking, Payment

        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')

        booking = Booking.objects.create(
            owner=self.owner,
            caretaker=self.caretaker_profile,
            pet=self.pet,
            service_type='Dog Walking',
            start_date=timezone.now().date() + timedelta(days=7),
            end_date=timezone.now().date() + timedelta(days=7),
            start_time='10:00:00',
            end_time='11:00:00',
            total_price=250.00,
            status='PENDING',
            payment_status='UNPAID'
        )

        failed_url = reverse('bookings:payment_failed', kwargs={'booking_id': booking.id})
        fail_payload = {
            'razorpay_order_id': 'order_failed_test_1',
            'error_code': 'BAD_REQUEST_ERROR',
            'error_description': 'Payment cancelled by user in UPI screen',
            'error_source': 'customer'
        }
        res = self.client.post(failed_url, data=json.dumps(fail_payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)

        booking.refresh_from_db()
        self.assertEqual(booking.payment_status, 'FAILED')
        self.assertFalse(booking.is_paid)

        payment = Payment.objects.get(booking=booking)
        self.assertEqual(payment.status, 'FAILED')
        self.assertEqual(payment.error_code, 'BAD_REQUEST_ERROR')
        self.assertIn('cancelled by user', payment.error_description)

    def test_pet_owner_registration_flow(self):
        """Test pet owner registration, backend assignment, and auto-login to dashboard."""
        reg_url = reverse('users:register')
        post_data = {
            'form_role': 'owner',
            'username': 'autotest_owner_1',
            'email': 'autotest_owner_1@example.com',
            'first_name': 'Alice',
            'last_name': 'Owner',
            'phone': '+91 98765 43210',
            'address': 'Chennai, Tamil Nadu',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        res = self.client.post(reg_url, data=post_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(User.objects.filter(username='autotest_owner_1').exists())
        user = User.objects.get(username='autotest_owner_1')
        self.assertEqual(user.role, 'PET_OWNER')
        self.assertTrue(user.is_pet_owner)
        self.assertIn('/users/dashboard/', [step[0] for step in res.redirect_chain])

    def test_caretaker_registration_flow(self):
        """Test caretaker registration, profile creation, and auto-login to caretaker dashboard."""
        reg_url = reverse('users:register')
        post_data = {
            'form_role': 'caretaker',
            'username': 'autotest_caretaker_1',
            'email': 'autotest_ct_1@example.com',
            'first_name': 'Bob',
            'last_name': 'Care',
            'phone': '+91 98765 43211',
            'address': 'Bengaluru, Karnataka',
            'experience_years': '4.5',
            'hourly_rate': '650.00',
            'services_offered': 'Pet Sitting, Dog Walking, Overnight Boarding',
            'bio': 'Passionate animal lover with 4+ years of veterinary assistance.',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        res = self.client.post(reg_url, data=post_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(User.objects.filter(username='autotest_caretaker_1').exists())
        user = User.objects.get(username='autotest_caretaker_1')
        self.assertEqual(user.role, 'CARETAKER')
        self.assertTrue(user.is_caretaker_user)
        self.assertTrue(hasattr(user, 'caretaker_profile'))
        self.assertEqual(float(user.caretaker_profile.hourly_rate), 650.00)
        self.assertEqual(float(user.caretaker_profile.experience_years), 4.5)
        self.assertIn('/users/dashboard/', [step[0] for step in res.redirect_chain])

    def test_registration_validation_errors(self):
        """Test validation error handling on registration form."""
        reg_url = reverse('users:register')
        # Mismatched passwords
        post_data = {
            'form_role': 'owner',
            'username': 'mismatch_user',
            'email': 'mismatch@example.com',
            'password': 'Password123!',
            'confirm_password': 'DifferentPassword456!'
        }
        res = self.client.post(reg_url, data=post_data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatch_user').exists())
        self.assertContains(res, "Passwords do not match")

    def test_adoption_catalog_and_inquiry_flow(self):
        """Test dynamic pet adoption catalog, filters, my-listings, and application inquiry."""
        from adoption.models import AdoptionListing
        from notifications.models import Notification

        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')

        # 1. Create a dynamic test adoption listing
        listing = AdoptionListing.objects.create(
            owner=self.caretaker_user,
            pet_name='Buster',
            species='Dog',
            breed='Labrador Retriever',
            age=1.5,
            gender='Male',
            listing_type='ADOPTION',
            price=0.00,
            location='Besant Nagar, Chennai',
            vaccination_status='Fully Vaccinated & Dewormed',
            description='Friendly energetic Lab looking for an active family!',
            contact_phone='+91 99999 11111',
            contact_email='caretaker@test.com',
            status='ACTIVE'
        )

        # 2. Browse Catalog
        catalog_url = reverse('adoption:listing_list')
        res_cat = self.client.get(catalog_url)
        self.assertEqual(res_cat.status_code, 200)
        self.assertContains(res_cat, "Buster")
        self.assertContains(res_cat, "Labrador Retriever")
        self.assertContains(res_cat, "Besant Nagar, Chennai")

        # 3. Filter by species
        res_filter = self.client.get(f"{catalog_url}?species=Dog")
        self.assertEqual(res_filter.status_code, 200)
        self.assertContains(res_filter, "Buster")

        # 4. View Detail Page
        detail_url = reverse('adoption:listing_detail', kwargs={'pk': listing.pk})
        res_detail = self.client.get(detail_url)
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, "Buster")
        self.assertContains(res_detail, "Apply to Adopt Buster")

        # 5. Submit Adoption Application
        inquire_url = reverse('adoption:submit_inquiry', kwargs={'pk': listing.pk})
        inquiry_data = {
            'applicant_name': 'Test Owner Alice',
            'applicant_email': 'owner@test.com',
            'applicant_phone': '+91 98765 00000',
            'housing_type': 'Independent House with Fenced Yard',
            'pet_experience': 'Experienced with pets',
            'message': 'We have a huge fenced yard and would love to welcome Buster into our home!'
        }
        res_inquire = self.client.post(inquire_url, data=inquiry_data, follow=True)
        self.assertEqual(res_inquire.status_code, 200)

        # Confirm notification delivered to pet guardian
        guardian_notif = Notification.objects.filter(
            user=listing.owner,
            notification_type='GENERAL'
        ).first()
        self.assertIsNotNone(guardian_notif)
        self.assertIn('Buster', guardian_notif.title)
        self.assertIn('Test Owner Alice', guardian_notif.message)
        self.assertIn('fenced yard', guardian_notif.message)

        # 6. Test My Listings view for guardian
        self.client.force_login(self.caretaker_user, backend='users.backends.EmailOrUsernameModelBackend')
        my_url = reverse('adoption:my_listings')
        res_my = self.client.get(my_url)
        self.assertEqual(res_my.status_code, 200)
        self.assertContains(res_my, "Buster")
        self.assertContains(res_my, "My Adoption &amp; Pet Listings")

    def test_adoption_payment_workflow(self):
        """Test full Razorpay payment workflow for pet adoption fee with HMAC-SHA256 verification."""
        from adoption.models import AdoptionListing, AdoptionPayment
        from bookings.payment_service import compute_expected_signature
        from notifications.models import Notification

        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')

        # 1. Create a fee-based adoption listing
        listing = AdoptionListing.objects.create(
            owner=self.caretaker_user,
            pet_name='Luna the Beagle',
            species='Dog',
            breed='Beagle',
            age=2.0,
            gender='Female',
            listing_type='ADOPTION',
            price=1500.00,
            location='Indiranagar, Bengaluru',
            vaccination_status='Fully Vaccinated & Microchipped',
            description='Loving Beagle, vaccinated, adoption fee covers medical & shelter costs.',
            contact_phone='+91 98888 22222',
            contact_email='shelter@test.com',
            status='ACTIVE',
            payment_status='UNPAID'
        )
        self.assertTrue(listing.requires_payment)
        self.assertFalse(listing.is_paid)

        # 2. View Adoption Checkout Page before request acceptance -> Must be LOCKED
        payment_url = reverse('adoption:payment', kwargs={'pk': listing.pk})
        res_locked = self.client.get(payment_url)
        self.assertEqual(res_locked.status_code, 200)
        self.assertContains(res_locked, "Payment Locked")

        # 3. Adopter submits adoption application
        inquire_url = reverse('adoption:submit_inquiry', kwargs={'pk': listing.pk})
        self.client.post(inquire_url, {
            'applicant_name': 'Test Owner Alice',
            'applicant_email': 'owner@test.com',
            'applicant_phone': '+91 98888 77777',
            'housing_type': 'Individual House',
            'pet_experience': '5 years with dogs',
            'message': 'We love Luna!'
        })
        adopt_req = listing.adoption_requests.get(applicant=self.owner)
        self.assertEqual(adopt_req.status, 'PENDING')

        # 4. Pet Owner logs in and accepts the request -> UNLOCKS payment
        self.client.force_login(self.caretaker_user, backend='users.backends.EmailOrUsernameModelBackend')
        accept_url = reverse('adoption:handle_request', kwargs={'request_id': adopt_req.id, 'action': 'accept'})
        res_accept = self.client.get(accept_url, follow=True)
        self.assertEqual(res_accept.status_code, 200)
        adopt_req.refresh_from_db()
        self.assertEqual(adopt_req.status, 'ACCEPTED')

        # 5. Adopter logs back in and visits checkout -> Payment is now UNLOCKED!
        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')
        res_page = self.client.get(payment_url)
        self.assertEqual(res_page.status_code, 200)
        self.assertContains(res_page, "1500.00")
        self.assertContains(res_page, "Pay Adoption Fee Now")
        self.assertContains(res_page, "Non-Refundable Adoption Fee Policy")
        self.assertContains(res_page, "Luna the Beagle")

        # Verify pending AdoptionPayment record was created in the database
        payment = AdoptionPayment.objects.get(listing=listing, adopter=self.owner)
        self.assertEqual(payment.status, 'PENDING')
        self.assertEqual(float(payment.amount), 1500.00)
        self.assertTrue(payment.razorpay_order_id.startswith('order_adopt_') or payment.razorpay_order_id.startswith('order_'))

        # 3. Test Invalid Signature Rejection
        verify_url = reverse('adoption:verify_payment', kwargs={'pk': listing.pk})
        invalid_payload = {
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': 'pay_adpt_fraud_001',
            'razorpay_signature': 'invalid_tampered_signature_99999',
            'payment_method': 'UPI'
        }
        res_invalid = self.client.post(verify_url, data=json.dumps(invalid_payload), content_type='application/json')
        self.assertEqual(res_invalid.status_code, 400)
        data_invalid = res_invalid.json()
        self.assertEqual(data_invalid['status'], 'error')

        listing.refresh_from_db()
        self.assertFalse(listing.is_paid)
        self.assertEqual(listing.status, 'ACTIVE')

        # 4. Test Valid Payment Verification with HMAC-SHA256
        test_payment_id = f"pay_adpt_{listing.id}_verified789"
        valid_signature = compute_expected_signature(payment.razorpay_order_id, test_payment_id)
        valid_payload = {
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': test_payment_id,
            'razorpay_signature': valid_signature,
            'payment_method': 'Google Pay (UPI / Tez)'
        }
        res_valid = self.client.post(verify_url, data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(res_valid.status_code, 200)
        data_valid = res_valid.json()
        self.assertEqual(data_valid['status'], 'success')
        self.assertIn('redirect_url', data_valid)

        # 5. Check Database Updates
        listing.refresh_from_db()
        payment.refresh_from_db()
        self.assertEqual(listing.status, 'ADOPTED')
        self.assertEqual(listing.payment_status, 'PAID')
        self.assertEqual(listing.adopter, self.owner)
        self.assertTrue(listing.is_paid)
        self.assertFalse(listing.requires_payment)

        self.assertEqual(payment.status, 'SUCCESS')
        self.assertEqual(payment.razorpay_payment_id, test_payment_id)
        self.assertEqual(payment.payment_method, 'Google Pay (UPI / Tez)')
        self.assertIsNotNone(payment.paid_at)

        # 6. Verify Notifications Dispatched to Adopter & Guardian
        adopter_notif = Notification.objects.filter(user=self.owner, notification_type='GENERAL').order_by('-created_at').first()
        self.assertIsNotNone(adopter_notif)
        self.assertIn("Adoption Confirmed", adopter_notif.title)
        self.assertIn("Luna the Beagle", adopter_notif.message)

        guardian_notif = Notification.objects.filter(user=self.caretaker_user, notification_type='GENERAL').order_by('-created_at').first()
        self.assertIsNotNone(guardian_notif)
        self.assertIn("Adoption Fee Received", guardian_notif.title)
        self.assertIn("1500.00", guardian_notif.message)

        # 7. Verify Checkout Page Now Displays Verified Receipt
        res_receipt = self.client.get(payment_url)
        self.assertEqual(res_receipt.status_code, 200)
        self.assertContains(res_receipt, "Adoption Fee Paid &amp; Verified")
        self.assertContains(res_receipt, "PAID &amp; CONFIRMED")
        self.assertContains(res_receipt, test_payment_id)

    def test_adoption_payment_failure_recording(self):
        """Test recording of failed/cancelled adoption payment attempts."""
        from adoption.models import AdoptionListing, AdoptionPayment

        self.client.force_login(self.owner, backend='users.backends.EmailOrUsernameModelBackend')

        listing = AdoptionListing.objects.create(
            owner=self.caretaker_user,
            pet_name='Milo the Kitten',
            species='Cat',
            breed='Persian',
            age=0.5,
            gender='Male',
            listing_type='ADOPTION',
            price=2000.00,
            location='Koramangala, Bengaluru',
            vaccination_status='First Dose Done',
            description='Playful kitten.',
            contact_phone='+91 97777 33333',
            contact_email='shelter2@test.com',
            status='ACTIVE',
            payment_status='UNPAID'
        )

        failed_url = reverse('adoption:payment_failed', kwargs={'pk': listing.pk})
        fail_payload = {
            'razorpay_order_id': 'order_adpt_fail_test_1',
            'error_code': 'PAYMENT_CANCELLED_BY_USER',
            'error_description': 'Customer dismissed UPI authorization prompt',
            'error_source': 'customer'
        }
        res = self.client.post(failed_url, data=json.dumps(fail_payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'recorded')

        listing.refresh_from_db()
        self.assertEqual(listing.payment_status, 'UNPAID')
        self.assertEqual(listing.status, 'ACTIVE')

        payment = AdoptionPayment.objects.get(listing=listing)
        self.assertEqual(payment.status, 'FAILED')
        self.assertEqual(payment.error_code, 'PAYMENT_CANCELLED_BY_USER')
        self.assertIn('dismissed UPI', payment.error_description)











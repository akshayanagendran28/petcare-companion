"""
End-to-End System Test Suite for Pet Care Companion
Tests Views, Authentication, Bookings, ML Inference, Breed Classifier, QR codes, and APIs.
"""

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
        self.assertContains(res, "maximum daily limit of 2 pets reached")

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








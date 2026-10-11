"""
Management Command: seed_data
Populates rich, realistic sample data for Pet Care Companion platform:
- Pet Owners and Caretakers
- Verified Caretaker Profiles
- Pets with auto-generated QR Codes
- Health Records (Vaccines, Weights, Medicines, Conditions)
- Bookings and Verified Reviews
- Adoption Listings
- Match Hub Profiles & Requests
- Lost Pet Reports & Sightings
- Notifications & Chat History
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from marketplace.models import CaretakerProfile
from pets.models import Pet
from bookings.models import Booking
from reviews.models import Review
from adoption.models import AdoptionListing
from matchhub.models import MatchProfile, MatchRequest
from health.models import HealthRecord, VaccinationRecord, MedicineRecord, WeightRecord, AllergyRecord
from lostfound.models import LostPetReport, LostPetSighting
from notifications.models import Notification
from chatbot.models import ChatHistory

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds realistic sample data for Pet Care Companion platform demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Pet Care Companion sample data..."))

        # 1. Create Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@petcarecompanion.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('Admin123#')
        admin_user.save()

        # 2. Create Pet Owners
        owner_sarah, _ = User.objects.get_or_create(
            username='sarah_jenkins',
            defaults={
                'email': 'sarah.jenkins@example.com',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'role': 'PET_OWNER',
                'phone': '+91 98450 11223',
                'address': 'Koramangala 4th Block, Bengaluru, KA',
            }
        )
        owner_sarah.set_password('PetOwner123#')
        owner_sarah.save()

        owner_david, _ = User.objects.get_or_create(
            username='david_miller',
            defaults={
                'email': 'david.miller@example.com',
                'first_name': 'David',
                'last_name': 'Miller',
                'role': 'PET_OWNER',
                'phone': '+91 97312 34567',
                'address': 'Indiranagar 100ft Rd, Bengaluru, KA',
            }
        )
        owner_david.set_password('PetOwner123#')
        owner_david.save()

        owner_priya, _ = User.objects.get_or_create(
            username='priya_sharma',
            defaults={
                'email': 'priya.sharma@example.com',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': 'PET_OWNER',
                'phone': '+91 99001 23456',
                'address': 'Bandra West, Mumbai, MH',
            }
        )
        owner_priya.set_password('PetOwner123#')
        owner_priya.save()

        # 3. Create Caretakers & Profiles
        caretakers_data = [
            {
                'username': 'alex_rivera',
                'email': 'alex.rivera@example.com',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'phone': '+91 98765 43210',
                'address': 'Koramangala, Bengaluru, KA',
                'exp': 4.5,
                'rate': 550.00,
                'services': 'Pet Sitting, Dog Walking, Agility Play, Daycare',
                'status': 'AVAILABLE',
                'bio': 'Certified veterinary technician assistant with 4+ years of hands-on pet sitting experience. Passionate about keeping energetic dogs active and giving cats peaceful attention.',
                'rating': 4.95,
                'reviews_cnt': 28,
                'earnings': 28500.00
            },
            {
                'username': 'elena_rostova',
                'email': 'elena.rostova@example.com',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'phone': '+91 91234 56780',
                'address': 'Indiranagar, Bengaluru, KA',
                'exp': 6.0,
                'rate': 750.00,
                'services': 'Senior Pet Care, Overnight Boarding, Medication Administration, Grooming',
                'status': 'AVAILABLE',
                'bio': 'Specialized senior pet and post-surgery care provider. Experienced in administering oral and subcutaneous medications with extreme gentleness and precision.',
                'rating': 5.00,
                'reviews_cnt': 42,
                'earnings': 45000.00
            },
            {
                'username': 'marcus_vance',
                'email': 'marcus.vance@example.com',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'phone': '+91 99887 76655',
                'address': 'HSR Layout, Bengaluru, KA',
                'exp': 3.0,
                'rate': 450.00,
                'services': 'High-Energy Dog Walking, Puppy Training, Adventure Hikes',
                'status': 'AVAILABLE',
                'bio': 'Canine fitness enthusiast who loves trail running and agility training with active large breeds like Huskies, Shepherds, and Labradors.',
                'rating': 4.85,
                'reviews_cnt': 19,
                'earnings': 18000.00
            },
            {
                'username': 'chloe_bennett',
                'email': 'chloe.bennett@example.com',
                'first_name': 'Chloe',
                'last_name': 'Bennett',
                'phone': '+91 98450 12345',
                'address': 'Whitefield, Bengaluru, KA',
                'exp': 2.5,
                'rate': 400.00,
                'services': 'Cat Sitting, Gentle In-Home Sitting, Grooming & Bath',
                'status': 'BUSY',
                'bio': 'Feline behavior specialist. Expert in shy and nervous cats, administering brush-outs, and gentle cuddles in a stress-free home environment.',
                'rating': 4.90,
                'reviews_cnt': 16,
                'earnings': 14500.00
            }
        ]

        caretaker_objs = []
        for c in caretakers_data:
            c_user, _ = User.objects.get_or_create(
                username=c['username'],
                defaults={
                    'email': c['email'],
                    'first_name': c['first_name'],
                    'last_name': c['last_name'],
                    'role': 'CARETAKER',
                    'phone': c['phone'],
                    'address': c['address'],
                }
            )
            c_user.set_password('Caretaker123#')
            c_user.save()

            c_profile, _ = CaretakerProfile.objects.get_or_create(
                user=c_user,
                defaults={
                    'experience_years': c['exp'],
                    'hourly_rate': c['rate'],
                    'services_offered': c['services'],
                    'availability_status': c['status'],
                    'bio': c['bio'],
                    'rating': c['rating'],
                    'total_reviews': c['reviews_cnt'],
                    'total_earnings': c['earnings'],
                }
            )
            caretaker_objs.append(c_profile)

        # 4. Create Pets (with auto QR Codes)
        pets_data = [
            {
                'owner': owner_sarah,
                'name': 'Max',
                'species': 'Dog',
                'breed': 'Golden Retriever',
                'age': 3.5,
                'gender': 'Male',
                'weight': 31.0,
                'health': 'Healthy',
                'activity': 'High',
                'vaccine_status': 'Up to Date',
                'allergies': 'None',
                'notes': 'Loves fetch in the lake! Microchipped #9851410029384.'
            },
            {
                'owner': owner_sarah,
                'name': 'Luna',
                'species': 'Cat',
                'breed': 'Persian Cat',
                'age': 2.0,
                'gender': 'Female',
                'weight': 4.2,
                'health': 'Sensitive Stomach / Allergies',
                'activity': 'Low',
                'vaccine_status': 'Up to Date',
                'allergies': 'Chicken & Dairy protein',
                'notes': 'Daily coat brushing required. Indoor only.'
            },
            {
                'owner': owner_david,
                'name': 'Rocky',
                'species': 'Dog',
                'breed': 'German Shepherd',
                'age': 4.0,
                'gender': 'Male',
                'weight': 36.5,
                'health': 'Healthy',
                'activity': 'Very High',
                'vaccine_status': 'Due Soon',
                'allergies': 'None',
                'notes': 'Very obedient. Protects family backyard.'
            },
            {
                'owner': owner_priya,
                'name': 'Bella',
                'species': 'Dog',
                'breed': 'French Bulldog',
                'age': 2.5,
                'gender': 'Female',
                'weight': 12.0,
                'health': 'Overweight',
                'activity': 'Low',
                'vaccine_status': 'Up to Date',
                'allergies': 'Beef',
                'notes': 'Avoid overheating during hot afternoons.'
            },
        ]

        pet_objs = []
        for p in pets_data:
            pet, _ = Pet.objects.get_or_create(
                owner=p['owner'],
                name=p['name'],
                defaults={
                    'species': p['species'],
                    'breed': p['breed'],
                    'age': p['age'],
                    'gender': p['gender'],
                    'weight': p['weight'],
                    'health_condition': p['health'],
                    'activity_level': p['activity'],
                    'vaccination_status': p['vaccine_status'],
                    'allergies': p['allergies'],
                    'medical_notes': p['notes'],
                }
            )
            pet_objs.append(pet)

        # 5. Create Health Records & Reminders
        today = timezone.now().date()
        max_pet = pet_objs[0] # Max
        luna_pet = pet_objs[1] # Luna
        rocky_pet = pet_objs[2] # Rocky

        # Vaccinations
        VaccinationRecord.objects.get_or_create(
            pet=max_pet,
            vaccine_name='Rabies 3-Year Booster',
            defaults={
                'administered_date': today - timedelta(days=300),
                'next_due_date': today + timedelta(days=795),
                'batch_number': 'RAB-9923',
                'vet_name': 'Dr. Emily Watson (Austin Animal Care)'
            }
        )
        VaccinationRecord.objects.get_or_create(
            pet=max_pet,
            vaccine_name='DHPP Core Vaccine',
            defaults={
                'administered_date': today - timedelta(days=350),
                'next_due_date': today + timedelta(days=15),  # Due Soon!
                'batch_number': 'DHPP-5401',
                'vet_name': 'Dr. Emily Watson'
            }
        )
        VaccinationRecord.objects.get_or_create(
            pet=rocky_pet,
            vaccine_name='Bordetella Kennel Cough',
            defaults={
                'administered_date': today - timedelta(days=190),
                'next_due_date': today - timedelta(days=10),  # Overdue!
                'batch_number': 'BORD-1122',
                'vet_name': 'Dr. Robert Hayes'
            }
        )

        # Weight History for Max
        for w_offset, w_val in [(120, 29.5), (90, 30.0), (60, 30.4), (30, 30.8), (0, 31.0)]:
            WeightRecord.objects.get_or_create(
                pet=max_pet,
                recorded_date=today - timedelta(days=w_offset),
                defaults={'weight_kg': w_val, 'notes': 'Routine weigh-in'}
            )

        # Active Medicine for Luna
        MedicineRecord.objects.get_or_create(
            pet=luna_pet,
            medicine_name='Probiotic GI Powder',
            defaults={
                'dosage': '1 scoop (5g)',
                'frequency': 'Once daily mixed in wet food',
                'start_date': today - timedelta(days=10),
                'end_date': today + timedelta(days=20),
                'notes': 'Restores healthy intestinal gut flora',
                'is_active': True,
            }
        )

        # 6. Create Bookings & Reviews
        booking_completed, _ = Booking.objects.get_or_create(
            owner=owner_sarah,
            caretaker=caretaker_objs[0], # Alex Rivera
            pet=max_pet,
            start_date=today - timedelta(days=14),
            end_date=today - timedelta(days=12),
            defaults={
                'service_type': 'Pet Sitting',
                'start_time': '09:00 AM',
                'end_time': '06:00 PM',
                'total_price': 3300.00,
                'notes': 'Max was super excited and well taken care of!',
                'status': 'COMPLETED',
            }
        )

        Review.objects.get_or_create(
            booking=booking_completed,
            defaults={
                'reviewer': owner_sarah,
                'caretaker': caretaker_objs[0],
                'rating': 5,
                'comment': 'Alex was phenomenal! Sent multiple daily photo updates of Max playing in the yard. Highly recommended!'
            }
        )

        # Upcoming Booking
        Booking.objects.get_or_create(
            owner=owner_sarah,
            caretaker=caretaker_objs[1], # Elena Rostova
            pet=luna_pet,
            start_date=today + timedelta(days=5),
            end_date=today + timedelta(days=8),
            defaults={
                'service_type': 'Overnight Boarding',
                'start_time': '10:00 AM',
                'end_time': '04:00 PM',
                'total_price': 4500.00,
                'notes': 'Luna needs her probiotic powder daily.',
                'status': 'ACCEPTED',
            }
        )

        # Pending Booking Request
        Booking.objects.get_or_create(
            owner=owner_david,
            caretaker=caretaker_objs[0], # Alex Rivera
            pet=rocky_pet,
            start_date=today + timedelta(days=2),
            end_date=today + timedelta(days=3),
            defaults={
                'service_type': 'Dog Walking',
                'start_time': '08:00 AM',
                'end_time': '12:00 PM',
                'total_price': 1800.00,
                'notes': 'Need morning agility walk around Cubbon Park.',
                'status': 'PENDING',
            }
        )

        # 7. Create Adoption Listings
        AdoptionListing.objects.get_or_create(
            pet_name='Daisy',
            defaults={
                'owner': owner_david,
                'species': 'Dog',
                'breed': 'Beagle',
                'age': 0.8,
                'gender': 'Female',
                'listing_type': 'ADOPTION',
                'price': 0.00,
                'location': 'Bengaluru, Karnataka',
                'vaccination_status': 'Fully Vaccinated & Microchipped',
                'description': 'Daisy is a merry, sweet Beagle puppy looking for a loving home with a yard. Loves kids and get along with other dogs.',
                'contact_phone': '+91 97312 34567',
                'contact_email': 'david.miller@example.com',
                'status': 'ACTIVE',
            }
        )

        AdoptionListing.objects.get_or_create(
            pet_name='Simba',
            defaults={
                'owner': owner_priya,
                'species': 'Cat',
                'breed': 'Maine Coon',
                'age': 1.2,
                'gender': 'Male',
                'listing_type': 'ADOPTION',
                'price': 0.00,
                'location': 'Mumbai, Maharashtra',
                'vaccination_status': 'Up to date',
                'description': 'Gentle giant Maine Coon! Very affectionate, purrs constantly, and enjoys company.',
                'contact_phone': '+91 99001 23456',
                'contact_email': 'priya.sharma@example.com',
                'status': 'ACTIVE',
            }
        )

        # 8. Create Match Profiles
        max_profile, _ = MatchProfile.objects.get_or_create(
            pet=max_pet,
            defaults={
                'looking_for': 'Playmate & Walking Buddy',
                'location': 'Cubbon Park, Bengaluru',
                'bio': 'Max is an outgoing Golden who loves playing fetch and swimming. Looking for friendly park playmates on weekends!',
                'is_active': True,
            }
        )

        rocky_profile, _ = MatchProfile.objects.get_or_create(
            pet=rocky_pet,
            defaults={
                'looking_for': 'Agility / Training Partner',
                'location': 'Lalbagh Botanical Gardens, Bengaluru',
                'bio': 'Athletic German Shepherd looking for agility training companions and group hiking buddies.',
                'is_active': True,
            }
        )

        # Match Request
        MatchRequest.objects.get_or_create(
            sender_profile=max_profile,
            receiver_profile=rocky_profile,
            defaults={
                'message': 'Hi David! Would love to get Max and Rocky together for a playdate at Cubbon Park this Saturday!',
                'status': 'PENDING',
            }
        )

        # 9. Create Lost & Found Report & Community Sighting
        lost_report, _ = LostPetReport.objects.get_or_create(
            pet_name='Ghost',
            defaults={
                'reporter': owner_priya,
                'species': 'Dog',
                'breed': 'Siberian Husky',
                'last_seen_location': 'Near Carter Road Promenade, Bandra, Mumbai',
                'date_lost': today - timedelta(days=2),
                'description': 'Ghost has bright blue eyes and a black/silver coat with a reflective blue collar. Skittish around sudden loud noises but friendly.',
                'contact_number': '+91 99001 23456',
                'reward_amount': 5000.00,
                'status': 'LOST',
            }
        )

        LostPetSighting.objects.get_or_create(
            lost_pet=lost_report,
            reporter_name='Officer Kevin Miller',
            defaults={
                'reporter_contact': 'kmiller@austincity.org',
                'sighting_location': 'Near Spyglass Trail Access Point',
                'sighting_date': today - timedelta(days=1),
                'description': 'Spotted a silver husky matching Ghost heading south toward the creek around 4:30 PM. Looked healthy and alert.',
            }
        )

        # 10. Sample Notifications
        Notification.objects.get_or_create(
            user=owner_sarah,
            title="Vaccination Reminder Due Soon 💉",
            defaults={
                'message': f"DHPP Core Vaccine for Max is due in 15 days ({today + timedelta(days=15)}).",
                'notification_type': 'REMINDER',
                'link': '/health/reminders/',
                'is_read': False,
            }
        )

        Notification.objects.get_or_create(
            user=caretaker_objs[0].user, # Alex Rivera
            title="New Booking Request! 🐾",
            defaults={
                'message': f"David Miller requested a Dog Walking booking for Rocky on {today + timedelta(days=2)}.",
                'notification_type': 'BOOKING',
                'link': '/bookings/caretaker/requests/',
                'is_read': False,
            }
        )

        self.stdout.write(self.style.SUCCESS("Sample data successfully seeded!"))
        self.stdout.write(self.style.SUCCESS("""
Test Credentials Available:
-----------------------------------------------------------
Role          Username         Password       Sample Pet
-----------------------------------------------------------
Admin         admin            Admin123#      -
Pet Owner     sarah_jenkins    PetOwner123#   Max (Golden Retriever)
Pet Owner     david_miller     PetOwner123#   Rocky (German Shepherd)
Pet Owner     priya_sharma     PetOwner123#   Bella (French Bulldog)
Caretaker     alex_rivera      Caretaker123#  -
Caretaker     elena_rostova    Caretaker123#  -
-----------------------------------------------------------
        """))

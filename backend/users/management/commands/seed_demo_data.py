import os
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction

from pets.models import Pet
from marketplace.models import CaretakerProfile
from bookings.models import Booking
from reviews.models import Review
from health.models import (
    HealthRecord,
    VaccinationRecord,
    MedicineRecord,
    WeightRecord,
    AllergyRecord,
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with realistic demo data for 20 customers, 20 caretakers, pets, bookings, reviews, and health records.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=== Starting Demo Data Seeding ==='))
        
        with transaction.atomic():
            customers = self.seed_customers()
            caretakers = self.seed_caretakers()
            pets = self.seed_pets(customers)
            bookings = self.seed_bookings(customers, caretakers, pets)
            reviews = self.seed_reviews(bookings)
            health_records = self.seed_health_data(pets)
            lostfound_records = self.seed_lostfound_data(customers)

        self.stdout.write(self.style.SUCCESS(f"""
=== Demo Data Seeding Completed Successfully! ===
- Customers Created/Updated: {len(customers)}
- Caretakers Created/Updated: {len(caretakers)}
- Pets Created/Updated: {len(pets)}
- Bookings Created/Updated: {len(bookings)}
- Reviews Created/Updated: {len(reviews)}
- Health Records Created/Updated: {health_records}
- Lost & Found Reports Created/Updated: {lostfound_records}
"""))

    def seed_customers(self):
        self.stdout.write('Seeding 20 Customer Accounts...')
        customer_data = [
            {'username': 'customer01', 'email': 'customer01@example.com', 'first_name': 'Akash', 'last_name': 'Kumar', 'phone': '+91 98401 23401', 'address': '14, 2nd Avenue, Anna Nagar, Chennai, Tamil Nadu - 600040', 'photo': 'customers/customer_01.jpg'},
            {'username': 'customer02', 'email': 'customer02@example.com', 'first_name': 'Divya', 'last_name': 'Krishnan', 'phone': '+91 98421 34502', 'address': '28, 80 Feet Road, KK Nagar, Madurai, Tamil Nadu - 625020', 'photo': 'customers/customer_02.jpg'},
            {'username': 'customer03', 'email': 'customer03@example.com', 'first_name': 'Rajesh', 'last_name': 'Kannan', 'phone': '+91 98940 45603', 'address': '45, DB Road, RS Puram, Coimbatore, Tamil Nadu - 641002', 'photo': 'customers/customer_03.jpg'},
            {'username': 'customer04', 'email': 'customer04@example.com', 'first_name': 'Meenakshi', 'last_name': 'Sundaram', 'phone': '+91 94431 56704', 'address': '9, Main Road, Thillai Nagar, Trichy, Tamil Nadu - 620018', 'photo': 'customers/customer_04.jpg'},
            {'username': 'customer05', 'email': 'customer05@example.com', 'first_name': 'Karthik', 'last_name': 'Rajan', 'phone': '+91 97890 67805', 'address': '72, Brindavan Road, Fairlands, Salem, Tamil Nadu - 636016', 'photo': 'customers/customer_05.jpg'},
            {'username': 'customer06', 'email': 'customer06@example.com', 'first_name': 'Ananya', 'last_name': 'Swaminathan', 'phone': '+91 96290 78906', 'address': '19, South Bye Pass Road, Palayamkottai, Tirunelveli, Tamil Nadu - 627002', 'photo': 'customers/customer_06.jpg'},
            {'username': 'customer07', 'email': 'customer07@example.com', 'first_name': 'Vigneshwaran', 'last_name': 'Balan', 'phone': '+91 99440 89007', 'address': '55, Srivilliputhur Road, Satchiyapuram, Sivakasi, Tamil Nadu - 626124', 'photo': 'customers/customer_07.jpg'},
            {'username': 'customer08', 'email': 'customer08@example.com', 'first_name': 'Shalini', 'last_name': 'Natarajan', 'phone': '+91 98430 90108', 'address': '31, GTN Salai, Dindigul, Tamil Nadu - 624005', 'photo': 'customers/customer_08.jpg'},
            {'username': 'customer09', 'email': 'customer09@example.com', 'first_name': 'Praveen', 'last_name': 'Chandran', 'phone': '+91 94420 01209', 'address': '84, Medical College Road, Thanjavur, Tamil Nadu - 613004', 'photo': 'customers/customer_09.jpg'},
            {'username': 'customer10', 'email': 'customer10@example.com', 'first_name': 'Kavitha', 'last_name': 'Murugan', 'phone': '+91 98427 12310', 'address': '112, Perundurai Road, Erode, Tamil Nadu - 638011', 'photo': 'customers/customer_10.jpg'},
            {'username': 'customer11', 'email': 'customer11@example.com', 'first_name': 'Senthil', 'last_name': 'Nathan', 'phone': '+91 99940 23411', 'address': '23, Kumaran Road, Tiruppur, Tamil Nadu - 641601', 'photo': 'customers/customer_11.jpg'},
            {'username': 'customer12', 'email': 'customer12@example.com', 'first_name': 'Deepika', 'last_name': 'Ramesh', 'phone': '+91 97870 34512', 'address': '67, Gandhi Nagar, Katpadi, Vellore, Tamil Nadu - 632014', 'photo': 'customers/customer_12.jpg'},
            {'username': 'customer13', 'email': 'customer13@example.com', 'first_name': 'Arunkumar', 'last_name': 'Veerappan', 'phone': '+91 94860 45613', 'address': '10, Court Road, Nagercoil, Tamil Nadu - 629001', 'photo': 'customers/customer_13.jpg'},
            {'username': 'customer14', 'email': 'customer14@example.com', 'first_name': 'Nithya', 'last_name': 'Subbiah', 'phone': '+91 98432 56714', 'address': '48, Jawahar Bazaar, Karur, Tamil Nadu - 639001', 'photo': 'customers/customer_14.jpg'},
            {'username': 'customer15', 'email': 'customer15@example.com', 'first_name': 'Saravanan', 'last_name': 'Govind', 'phone': '+91 96000 67815', 'address': '105, Gandhi Road, Kanchipuram, Tamil Nadu - 631501', 'photo': 'customers/customer_15.jpg'},
            {'username': 'customer16', 'email': 'customer16@example.com', 'first_name': 'Poornima', 'last_name': 'Selvam', 'phone': '+91 98424 78916', 'address': '18, TSR Big Street, Kumbakonam, Tamil Nadu - 612001', 'photo': 'customers/customer_16.jpg'},
            {'username': 'customer17', 'email': 'customer17@example.com', 'first_name': 'Balaji', 'last_name': 'Parthiban', 'phone': '+91 94433 89017', 'address': '92, Cruz Fernandez Avenue, Millerpuram, Thoothukudi, Tamil Nadu - 628008', 'photo': 'customers/customer_17.jpg'},
            {'username': 'customer18', 'email': 'customer18@example.com', 'first_name': 'Harini', 'last_name': 'Raman', 'phone': '+91 97500 90118', 'address': '34, New Scheme Road, Pollachi, Tamil Nadu - 642001', 'photo': 'customers/customer_18.jpg'},
            {'username': 'customer19', 'email': 'customer19@example.com', 'first_name': 'Vijay', 'last_name': 'Anand', 'phone': '+91 98945 01219', 'address': '51, Bagalur Road, Hosur, Tamil Nadu - 635109', 'photo': 'customers/customer_19.jpg'},
            {'username': 'customer20', 'email': 'customer20@example.com', 'first_name': 'Sneha', 'last_name': 'Manickam', 'phone': '+91 94437 12320', 'address': '8, Salai Street, Ramanathapuram, Tamil Nadu - 623501', 'photo': 'customers/customer_20.jpg'},
        ]

        created_users = []
        for d in customer_data:
            user, created = User.objects.get_or_create(username=d['username'])
            user.email = d['email']
            user.first_name = d['first_name']
            user.last_name = d['last_name']
            user.role = 'PET_OWNER'
            user.phone = d['phone']
            user.address = d['address']
            user.profile_photo = d['photo']
            user.set_password('Customer@123')
            user.save()
            created_users.append(user)
        return created_users

    def seed_caretakers(self):
        self.stdout.write('Seeding 20 Caretaker Accounts & Profiles...')
        caretaker_data = [
            {'username': 'caretaker01', 'email': 'caretaker01@example.com', 'first_name': 'Priya', 'last_name': 'Sharma', 'phone': '+91 98421 99001', 'address': '42, West Veli Street, Madurai, Tamil Nadu - 625001', 'photo': 'caretakers/caretaker_01.jpg', 'experience_years': Decimal('5.5'), 'hourly_rate': Decimal('500.00'), 'services_offered': 'Pet Sitting, Dog Walking, Feeding, Daycare', 'availability_status': 'AVAILABLE', 'bio': 'Certified canine behaviorist & pet nutritionist with 5+ years of dedicated pet care experience across Madurai.'},
            {'username': 'caretaker02', 'email': 'caretaker02@example.com', 'first_name': 'Suresh', 'last_name': 'Kumar', 'phone': '+91 98402 99002', 'address': '15, GST Road, Guindy, Chennai, Tamil Nadu - 600032', 'photo': 'caretakers/caretaker_02.jpg', 'experience_years': Decimal('7.0'), 'hourly_rate': Decimal('650.00'), 'services_offered': 'Pet Sitting, Dog Walking, Overnight Boarding, Grooming & Bath', 'availability_status': 'AVAILABLE', 'bio': 'Former veterinary technician offering specialized senior pet nursing, post-surgery care, and calm overnight boarding.'},
            {'username': 'caretaker03', 'email': 'caretaker03@example.com', 'first_name': 'Karthikeyan', 'last_name': 'Murugan', 'phone': '+91 98941 99003', 'address': '88, Avinashi Road, Peelamedu, Coimbatore, Tamil Nadu - 641004', 'photo': 'caretakers/caretaker_03.jpg', 'experience_years': Decimal('4.0'), 'hourly_rate': Decimal('450.00'), 'services_offered': 'Dog Walking, Daycare, Pet Sitting', 'availability_status': 'AVAILABLE', 'bio': 'Energetic dog fitness coach and trail runner. Your furry friend will enjoy long, stimulating outdoor exercise sessions.'},
            {'username': 'caretaker04', 'email': 'caretaker04@example.com', 'first_name': 'Deepa', 'last_name': 'Balaji', 'phone': '+91 94432 99004', 'address': '22, Cantonment, Trichy, Tamil Nadu - 620001', 'photo': 'caretakers/caretaker_04.jpg', 'experience_years': Decimal('6.2'), 'hourly_rate': Decimal('550.00'), 'services_offered': 'Pet Sitting, Feeding, Daycare, Grooming & Bath', 'availability_status': 'AVAILABLE', 'bio': 'Cat whisperer and small animal specialist. Calm, quiet home environment with multiple climbing trees and safe indoor zones.'},
            {'username': 'caretaker05', 'email': 'caretaker05@example.com', 'first_name': 'Ramesh', 'last_name': 'Varma', 'phone': '+91 97891 99005', 'address': '34, Omalur Main Road, Salem, Tamil Nadu - 636009', 'photo': 'caretakers/caretaker_05.jpg', 'experience_years': Decimal('3.5'), 'hourly_rate': Decimal('400.00'), 'services_offered': 'Dog Walking, Feeding, Pet Sitting', 'availability_status': 'AVAILABLE', 'bio': 'Punctual, friendly caretaker providing daily home check-ins, hydration monitoring, and medication administration.'},
            {'username': 'caretaker06', 'email': 'caretaker06@example.com', 'first_name': 'Preethi', 'last_name': 'Sundar', 'phone': '+91 96291 99006', 'address': '51, Trivandrum Road, Tirunelveli, Tamil Nadu - 627003', 'photo': 'caretakers/caretaker_06.jpg', 'experience_years': Decimal('8.0'), 'hourly_rate': Decimal('700.00'), 'services_offered': 'Pet Sitting, Overnight Boarding, Grooming & Bath', 'availability_status': 'AVAILABLE', 'bio': 'Professional pet groomer and fear-free certified handler. Spacious climate-controlled boarding facility.'},
            {'username': 'caretaker07', 'email': 'caretaker07@example.com', 'first_name': 'Manikandan', 'last_name': 'Raman', 'phone': '+91 99441 99007', 'address': '77, Chairman Shanmugam Road, Sivakasi, Tamil Nadu - 626123', 'photo': 'caretakers/caretaker_07.jpg', 'experience_years': Decimal('2.5'), 'hourly_rate': Decimal('350.00'), 'services_offered': 'Dog Walking, Pet Sitting, Feeding', 'availability_status': 'AVAILABLE', 'bio': 'Dedicated animal lover providing structured walks, engaging playtime, and loving attention to domestic pets.'},
            {'username': 'caretaker08', 'email': 'caretaker08@example.com', 'first_name': 'Gowri', 'last_name': 'Shankar', 'phone': '+91 98431 99008', 'address': '12, Palani Road, Dindigul, Tamil Nadu - 624001', 'photo': 'caretakers/caretaker_08.jpg', 'experience_years': Decimal('5.0'), 'hourly_rate': Decimal('480.00'), 'services_offered': 'Pet Sitting, Dog Walking, Daycare', 'availability_status': 'AVAILABLE', 'bio': 'Experienced in caring for large working breeds with tailored exercise and agility routines.'},
            {'username': 'caretaker09', 'email': 'caretaker09@example.com', 'first_name': 'Revathi', 'last_name': 'Nathan', 'phone': '+91 94421 99009', 'address': '90, South Main Street, Thanjavur, Tamil Nadu - 613009', 'photo': 'caretakers/caretaker_09.jpg', 'experience_years': Decimal('9.5'), 'hourly_rate': Decimal('750.00'), 'services_offered': 'Pet Sitting, Overnight Boarding, Grooming & Bath, Feeding', 'availability_status': 'AVAILABLE', 'bio': 'Senior pet nurse with nearly a decade of experience in dietary planning, emergency care, and loving boarding.'},
            {'username': 'caretaker10', 'email': 'caretaker10@example.com', 'first_name': 'Ashok', 'last_name': 'Selvan', 'phone': '+91 98428 99010', 'address': '64, Brough Road, Erode, Tamil Nadu - 638001', 'photo': 'caretakers/caretaker_10.jpg', 'experience_years': Decimal('3.0'), 'hourly_rate': Decimal('380.00'), 'services_offered': 'Dog Walking, Feeding, Daycare', 'availability_status': 'AVAILABLE', 'bio': 'Weekend sitter and energetic companion for dogs that love play sessions, ball fetch, and interactive brain puzzles.'},
            {'username': 'caretaker11', 'email': 'caretaker11@example.com', 'first_name': 'Bhuvaneshwari', 'last_name': 'K', 'phone': '+91 99941 99011', 'address': '38, Kangayam Road, Tiruppur, Tamil Nadu - 641604', 'photo': 'caretakers/caretaker_11.jpg', 'experience_years': Decimal('4.5'), 'hourly_rate': Decimal('520.00'), 'services_offered': 'Pet Sitting, Daycare, Grooming & Bath', 'availability_status': 'AVAILABLE', 'bio': 'Gentle handler for anxious and rescue pets. Focuses on positive reinforcement and stress-free socialization.'},
            {'username': 'caretaker12', 'email': 'caretaker12@example.com', 'first_name': 'Vignesh', 'last_name': 'Pandian', 'phone': '+91 97871 99012', 'address': '102, Officer Line, Vellore, Tamil Nadu - 632001', 'photo': 'caretakers/caretaker_12.jpg', 'experience_years': Decimal('6.0'), 'hourly_rate': Decimal('600.00'), 'services_offered': 'Overnight Boarding, Daycare, Pet Sitting', 'availability_status': 'AVAILABLE', 'bio': 'Secure home boarding with 24/7 camera monitoring, private grassy play yard, and constant companionship.'},
            {'username': 'caretaker13', 'email': 'caretaker13@example.com', 'first_name': 'Jayanthi', 'last_name': 'Ramanathan', 'phone': '+91 94861 99013', 'address': '26, Cape Road, Nagercoil, Tamil Nadu - 629002', 'photo': 'caretakers/caretaker_13.jpg', 'experience_years': Decimal('2.0'), 'hourly_rate': Decimal('300.00'), 'services_offered': 'Pet Sitting, Feeding, Dog Walking', 'availability_status': 'AVAILABLE', 'bio': 'Loving family environment for small dogs, puppies, and bunnies. Safe indoor playtime and constant affection.'},
            {'username': 'caretaker14', 'email': 'caretaker14@example.com', 'first_name': 'Anandhi', 'last_name': 'Muthukumar', 'phone': '+91 98433 99014', 'address': '81, Kovai Road, Karur, Tamil Nadu - 639002', 'photo': 'caretakers/caretaker_14.jpg', 'experience_years': Decimal('5.8'), 'hourly_rate': Decimal('540.00'), 'services_offered': 'Dog Walking, Pet Sitting, Overnight Boarding', 'availability_status': 'AVAILABLE', 'bio': 'Certified pet CPR and first responder. Real-time GPS walking routes and photo updates sent during every session.'},
            {'username': 'caretaker15', 'email': 'caretaker15@example.com', 'first_name': 'Dinesh', 'last_name': 'Chandran', 'phone': '+91 96001 99015', 'address': '14, Ekambaranathar Sannathi, Kanchipuram, Tamil Nadu - 631502', 'photo': 'caretakers/caretaker_15.jpg', 'experience_years': Decimal('3.8'), 'hourly_rate': Decimal('420.00'), 'services_offered': 'Dog Walking, Daycare, Feeding', 'availability_status': 'AVAILABLE', 'bio': 'Passionate walker who ensures your pets receive both physical exercise and mental stimulation.'},
            {'username': 'caretaker16', 'email': 'caretaker16@example.com', 'first_name': 'Geetha', 'last_name': 'Sridhar', 'phone': '+91 98425 99016', 'address': '55, Kumbeswarar South Street, Kumbakonam, Tamil Nadu - 612001', 'photo': 'caretakers/caretaker_16.jpg', 'experience_years': Decimal('7.5'), 'hourly_rate': Decimal('680.00'), 'services_offered': 'Pet Sitting, Grooming & Bath, Overnight Boarding', 'availability_status': 'AVAILABLE', 'bio': 'Holistic pet care practitioner offering organic home-cooked meals, gentle herbal bathing, and attentive care.'},
            {'username': 'caretaker17', 'email': 'caretaker17@example.com', 'first_name': 'Naveen', 'last_name': 'Prasath', 'phone': '+91 94434 99017', 'address': '43, Palayamkottai Road, Thoothukudi, Tamil Nadu - 628003', 'photo': 'caretakers/caretaker_17.jpg', 'experience_years': Decimal('1.8'), 'hourly_rate': Decimal('280.00'), 'services_offered': 'Dog Walking, Feeding', 'availability_status': 'BUSY', 'bio': 'Punctual, attentive morning walker with a focus on leash safety and hydration.'},
            {'username': 'caretaker18', 'email': 'caretaker18@example.com', 'first_name': 'Lakshmi', 'last_name': 'Narayanan', 'phone': '+91 97501 99018', 'address': '60, Meenkarai Road, Pollachi, Tamil Nadu - 642001', 'photo': 'caretakers/caretaker_18.jpg', 'experience_years': Decimal('6.5'), 'hourly_rate': Decimal('580.00'), 'services_offered': 'Overnight Boarding, Daycare, Dog Walking', 'availability_status': 'AVAILABLE', 'bio': 'Spacious countryside property with lush fenced run areas, natural swimming splash ponds, and agility ramps.'},
            {'username': 'caretaker19', 'email': 'caretaker19@example.com', 'first_name': 'Hariprasad', 'last_name': 'Swaminathan', 'phone': '+91 98946 99019', 'address': '118, Denkanikotta Road, Hosur, Tamil Nadu - 635109', 'photo': 'caretakers/caretaker_19.jpg', 'experience_years': Decimal('10.0'), 'hourly_rate': Decimal('800.00'), 'services_offered': 'Pet Sitting, Dog Walking, Overnight Boarding, Daycare', 'availability_status': 'AVAILABLE', 'bio': 'Master canine handler and trainer with 10 years in obedience instruction, agility, and premium boarding.'},
            {'username': 'caretaker20', 'email': 'caretaker20@example.com', 'first_name': 'Shalini', 'last_name': 'Vimal', 'phone': '+91 94438 99020', 'address': '29, Vandikkara Street, Ramanathapuram, Tamil Nadu - 623501', 'photo': 'caretakers/caretaker_20.jpg', 'experience_years': Decimal('4.2'), 'hourly_rate': Decimal('460.00'), 'services_offered': 'Pet Sitting, Feeding, Grooming & Bath', 'availability_status': 'AVAILABLE', 'bio': 'Compassionate neighborhood pet sitter offering overnight home stays and personalized grooming sessions.'},
        ]

        created_profiles = []
        for d in caretaker_data:
            user, created = User.objects.get_or_create(username=d['username'])
            user.email = d['email']
            user.first_name = d['first_name']
            user.last_name = d['last_name']
            user.role = 'CARETAKER'
            user.phone = d['phone']
            user.address = d['address']
            user.profile_photo = d['photo']
            user.set_password('Caretaker@123')
            user.save()

            profile, _ = CaretakerProfile.objects.get_or_create(user=user)
            profile.experience_years = d['experience_years']
            profile.hourly_rate = d['hourly_rate']
            profile.services_offered = d['services_offered']
            profile.availability_status = d['availability_status']
            profile.bio = d['bio']
            profile.save()
            created_profiles.append(profile)

        return created_profiles

    def seed_pets(self, customers):
        self.stdout.write('Seeding 48 Pets across Customers...')
        pets_blueprint = [
            (0, 'Bruno', 'Dog', 'Labrador Retriever', Decimal('3.0'), 'Male', Decimal('28.5'), 'Healthy', 'High', 'Up to Date', 'None', 'Very active and loves fetching tennis balls.', 'pets/pet_001.jpg'),
            (0, 'Luna', 'Cat', 'Persian Cat', Decimal('2.0'), 'Female', Decimal('4.2'), 'Healthy', 'Low', 'Up to Date', 'Dust sensitivity', 'Prefers quiet cozy corners and daily combing.', 'pets/pet_002.jpg'),
            (0, 'Coco', 'Rabbit', 'Holland Lop', Decimal('1.0'), 'Female', Decimal('1.8'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Loves fresh coriander and timothy hay.', 'pets/pet_003.jpg'),

            (1, 'Rocky', 'Dog', 'German Shepherd', Decimal('4.5'), 'Male', Decimal('34.0'), 'Healthy', 'Very High', 'Up to Date', 'None', 'Trained in basic obedience and agility.', 'pets/pet_004.jpg'),
            (1, 'Milo', 'Cat', 'Siamese Cat', Decimal('1.5'), 'Male', Decimal('3.8'), 'Healthy', 'Moderate', 'Due Soon', 'None', 'Very vocal and affectionate cat.', 'pets/pet_005.jpg'),

            (2, 'Simba', 'Dog', 'Golden Retriever', Decimal('2.5'), 'Male', Decimal('30.0'), 'Healthy', 'High', 'Up to Date', 'Chicken allergy', 'Feed hypoallergenic salmon formula only.', 'pets/pet_006.jpg'),
            (2, 'Bella', 'Dog', 'Beagle', Decimal('3.0'), 'Female', Decimal('12.0'), 'Healthy', 'High', 'Up to Date', 'None', 'Loves scent tracking games and belly rubs.', 'pets/pet_007.jpg'),
            (2, 'Kiwi', 'Bird', 'Cockatiel', Decimal('1.2'), 'Male', Decimal('0.10'), 'Healthy', 'Low', 'Up to Date', 'None', 'Whistles tunes when music is playing.', 'pets/pet_008.jpg'),

            (3, 'Charlie', 'Dog', 'Pug', Decimal('4.0'), 'Male', Decimal('9.5'), 'Healthy', 'Low', 'Overdue', 'None', 'Needs facial wrinkle cleaning twice a week.', 'pets/pet_009.jpg'),
            (3, 'Oliver', 'Cat', 'British Shorthair', Decimal('2.8'), 'Male', Decimal('5.5'), 'Healthy', 'Low', 'Up to Date', 'None', 'Calm and dignified lap cat.', 'pets/pet_010.jpg'),

            (4, 'Shadow', 'Dog', 'Indie', Decimal('2.0'), 'Male', Decimal('18.0'), 'Healthy', 'Very High', 'Up to Date', 'None', 'Rescued street pup, very resilient and agile.', 'pets/pet_011.jpg'),
            (4, 'Lily', 'Cat', 'Maine Coon', Decimal('3.5'), 'Female', Decimal('6.8'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Gentle giant with a thick winter coat.', 'pets/pet_012.jpg'),
            (4, 'Bunbun', 'Rabbit', 'Mini Rex', Decimal('1.5'), 'Female', Decimal('2.1'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Soft velvet coat, likes cardboard tunnels.', 'pets/pet_013.jpg'),

            (5, 'Daisy', 'Dog', 'Shih Tzu', Decimal('2.0'), 'Female', Decimal('6.2'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Requires daily eye wiping and gentle coat brushing.', 'pets/pet_014.jpg'),
            (5, 'Nala', 'Cat', 'Indie Cat', Decimal('1.0'), 'Female', Decimal('3.2'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Loves watching birds through the window.', 'pets/pet_015.jpg'),

            (6, 'Tyson', 'Dog', 'Rottweiler', Decimal('3.5'), 'Male', Decimal('42.0'), 'Healthy', 'High', 'Up to Date', 'None', 'Loyal guard companion, very gentle with family.', 'pets/pet_016.jpg'),
            (6, 'Oreo', 'Dog', 'Border Collie', Decimal('2.0'), 'Male', Decimal('19.5'), 'Healthy', 'Very High', 'Up to Date', 'None', 'Loves frisbee catches and obstacle courses.', 'pets/pet_017.jpg'),

            (7, 'Ginger', 'Cat', 'Tabby Cat', Decimal('2.2'), 'Female', Decimal('4.0'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Loves chasing laser pointer dots.', 'pets/pet_018.jpg'),
            (7, 'Rio', 'Bird', 'Lovebird', Decimal('0.8'), 'Male', Decimal('0.05'), 'Healthy', 'Low', 'Up to Date', 'None', 'Very active and chirps in the morning.', 'pets/pet_019.jpg'),

            (8, 'Cooper', 'Dog', 'Cocker Spaniel', Decimal('3.2'), 'Male', Decimal('13.5'), 'Healthy', 'High', 'Up to Date', 'Ear sensitivity', 'Keep ears clean and dry after baths.', 'pets/pet_020.jpg'),
            (8, 'Mia', 'Cat', 'Ragdoll', Decimal('1.8'), 'Female', Decimal('4.8'), 'Healthy', 'Low', 'Due Soon', 'None', 'Limp and relaxed when held.', 'pets/pet_021.jpg'),
            (8, 'Cheeku', 'Rabbit', 'Netherland Dwarf', Decimal('1.0'), 'Male', Decimal('1.2'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Compact bunny, likes apple wood chews.', 'pets/pet_022.jpg'),

            (9, 'Leo', 'Dog', 'Pomeranian', Decimal('4.0'), 'Male', Decimal('4.5'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Fluffy coat and alert barker.', 'pets/pet_023.jpg'),
            (9, 'Chloe', 'Cat', 'Birman', Decimal('2.5'), 'Female', Decimal('4.1'), 'Healthy', 'Low', 'Up to Date', 'None', 'Gentle sapphire-eyed beauty.', 'pets/pet_024.jpg'),

            (10, 'Buster', 'Dog', 'Boxer', Decimal('3.0'), 'Male', Decimal('30.5'), 'Healthy', 'High', 'Up to Date', 'None', 'Playful and loves jumping on trampoline.', 'pets/pet_025.jpg'),
            (10, 'Penny', 'Dog', 'Dachshund', Decimal('2.5'), 'Female', Decimal('8.0'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Avoid stairs to protect spine.', 'pets/pet_026.jpg'),

            (11, 'Casper', 'Cat', 'Russian Blue', Decimal('2.0'), 'Male', Decimal('4.5'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Silver shimmer coat, quiet companion.', 'pets/pet_027.jpg'),
            (11, 'Pip', 'Bird', 'Budgerigar', Decimal('1.0'), 'Male', Decimal('0.04'), 'Healthy', 'Low', 'Up to Date', 'None', 'Bright yellow budgie with cheerful chirps.', 'pets/pet_028.jpg'),

            (12, 'Thor', 'Dog', 'Siberian Husky', Decimal('2.8'), 'Male', Decimal('24.0'), 'Healthy', 'Very High', 'Up to Date', 'None', 'High energy, requires cool indoor space in summer.', 'pets/pet_029.jpg'),
            (12, 'Stella', 'Dog', 'Great Dane', Decimal('3.5'), 'Female', Decimal('52.0'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Gentle giant who thinks she is a lapdog.', 'pets/pet_030.jpg'),
            (12, 'Fluffy', 'Rabbit', 'Angora Rabbit', Decimal('1.2'), 'Female', Decimal('2.5'), 'Healthy', 'Low', 'Up to Date', 'None', 'Long wool requires weekly gentle grooming.', 'pets/pet_031.jpg'),

            (13, 'Zoe', 'Cat', 'Sphynx', Decimal('3.0'), 'Female', Decimal('3.6'), 'Healthy', 'High', 'Up to Date', 'Cold sensitivity', 'Keep indoors with warm sweaters during winter.', 'pets/pet_032.jpg'),
            (13, 'Cookie', 'Cat', 'Scottish Fold', Decimal('1.5'), 'Female', Decimal('3.9'), 'Healthy', 'Low', 'Up to Date', 'None', 'Folded ears and sweet temperament.', 'pets/pet_033.jpg'),

            (14, 'Bruno Jr', 'Dog', 'Doberman', Decimal('2.2'), 'Male', Decimal('36.0'), 'Healthy', 'Very High', 'Up to Date', 'None', 'Alert, highly trainable and intelligent.', 'pets/pet_034.jpg'),
            (14, 'Ruby', 'Dog', 'Cavalier King Charles', Decimal('1.8'), 'Female', Decimal('7.2'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Loving lap dog with silky ears.', 'pets/pet_035.jpg'),

            (15, 'Simba Cat', 'Cat', 'Bengal Cat', Decimal('2.0'), 'Male', Decimal('5.2'), 'Healthy', 'High', 'Up to Date', 'None', 'Leopard spotted coat and very agile climber.', 'pets/pet_036.jpg'),
            (15, 'Sunny', 'Bird', 'Sun Conure', Decimal('1.5'), 'Male', Decimal('0.12'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Vibrant orange and yellow feathers.', 'pets/pet_037.jpg'),

            (16, 'Maximus', 'Dog', 'Labrador Retriever', Decimal('4.0'), 'Male', Decimal('31.0'), 'Healthy', 'High', 'Up to Date', 'None', 'Loves swimming in lakes and retrieving sticks.', 'pets/pet_038.jpg'),
            (16, 'Snoopy', 'Dog', 'Beagle', Decimal('2.0'), 'Male', Decimal('11.5'), 'Healthy', 'High', 'Due Soon', 'None', 'Always following scent trails.', 'pets/pet_039.jpg'),
            (16, 'Snowball', 'Rabbit', 'Flemish Giant', Decimal('2.0'), 'Female', Decimal('4.8'), 'Healthy', 'Low', 'Up to Date', 'None', 'Calm giant rabbit, loves leafy greens.', 'pets/pet_040.jpg'),

            (17, 'Maya', 'Dog', 'Indie', Decimal('1.5'), 'Female', Decimal('16.5'), 'Healthy', 'High', 'Up to Date', 'None', 'Very smart, rescued from Coimbatore.', 'pets/pet_041.jpg'),
            (17, 'Cleo', 'Cat', 'Bombay Cat', Decimal('2.5'), 'Female', Decimal('3.9'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Sleek black panther look with copper eyes.', 'pets/pet_042.jpg'),

            (18, 'Rex', 'Dog', 'German Shepherd', Decimal('3.8'), 'Male', Decimal('35.5'), 'Healthy', 'Very High', 'Up to Date', 'None', 'Trained protection and family companion.', 'pets/pet_043.jpg'),
            (18, 'Penny Cat', 'Cat', 'Norwegian Forest Cat', Decimal('3.0'), 'Female', Decimal('6.0'), 'Healthy', 'Moderate', 'Up to Date', 'None', 'Dense water-resistant coat and bushy tail.', 'pets/pet_044.jpg'),

            (19, 'Teddy', 'Dog', 'Poodle', Decimal('2.0'), 'Male', Decimal('7.0'), 'Healthy', 'High', 'Up to Date', 'None', 'Hypoallergenic curly coat, loves agility runs.', 'pets/pet_045.jpg'),
            (19, 'Hazel', 'Cat', 'Abyssinian', Decimal('1.8'), 'Female', Decimal('3.5'), 'Healthy', 'High', 'Up to Date', 'None', 'Ruddy ticked coat and energetic jumper.', 'pets/pet_046.jpg'),
            (19, 'Mango', 'Bird', 'African Grey', Decimal('4.0'), 'Male', Decimal('0.40'), 'Healthy', 'Low', 'Up to Date', 'None', 'Remarkable vocabulary and mimicry skills.', 'pets/pet_047.jpg'),
        ]

        created_pets = []
        for cust_idx, name, species, breed, age, gender, weight, health, activity, vax, allergies, notes, photo in pets_blueprint:
            owner = customers[cust_idx]
            pet, _ = Pet.objects.get_or_create(
                owner=owner,
                name=name,
                defaults={
                    'species': species,
                    'breed': breed,
                    'age': age,
                    'gender': gender,
                    'weight': weight,
                    'health_condition': health,
                    'activity_level': activity,
                    'vaccination_status': vax,
                    'allergies': allergies,
                    'medical_notes': notes,
                    'photo': photo,
                }
            )
            pet.species = species
            pet.breed = breed
            pet.age = age
            pet.gender = gender
            pet.weight = weight
            pet.health_condition = health
            pet.activity_level = activity
            pet.vaccination_status = vax
            pet.allergies = allergies
            pet.medical_notes = notes
            pet.photo = photo
            pet.save()
            created_pets.append(pet)

        return created_pets

    def seed_bookings(self, customers, caretakers, pets):
        self.stdout.write('Seeding 40 Bookings across Statuses...')
        today = timezone.now().date()
        
        bookings_blueprint = [
            (0, 0, 0, 'Pet Sitting', -25, 3, 'COMPLETED', Decimal('1500.00')),
            (0, 0, 1, 'Daycare', -18, 2, 'COMPLETED', Decimal('1000.00')),
            (1, 0, 3, 'Dog Walking', -12, 1, 'COMPLETED', Decimal('500.00')),
            (2, 1, 5, 'Overnight Boarding', -30, 4, 'COMPLETED', Decimal('2600.00')),
            (3, 1, 8, 'Grooming & Bath', -22, 1, 'COMPLETED', Decimal('650.00')),
            (4, 2, 10, 'Dog Walking', -15, 2, 'COMPLETED', Decimal('900.00')),
            (5, 3, 13, 'Pet Sitting', -28, 3, 'COMPLETED', Decimal('1650.00')),
            (6, 4, 15, 'Dog Walking', -20, 1, 'COMPLETED', Decimal('400.00')),
            (7, 5, 17, 'Pet Sitting', -14, 2, 'COMPLETED', Decimal('1400.00')),
            (8, 6, 19, 'Dog Walking', -26, 3, 'COMPLETED', Decimal('1050.00')),
            (9, 7, 22, 'Daycare', -10, 2, 'COMPLETED', Decimal('960.00')),
            (10, 8, 24, 'Overnight Boarding', -32, 5, 'COMPLETED', Decimal('3750.00')),
            (11, 9, 26, 'Dog Walking', -16, 2, 'COMPLETED', Decimal('760.00')),
            (12, 10, 28, 'Pet Sitting', -21, 3, 'COMPLETED', Decimal('1560.00')),
            (13, 11, 31, 'Overnight Boarding', -19, 2, 'COMPLETED', Decimal('1200.00')),
            (14, 12, 33, 'Pet Sitting', -24, 2, 'COMPLETED', Decimal('600.00')),
            (15, 13, 35, 'Dog Walking', -11, 1, 'COMPLETED', Decimal('540.00')),
            (16, 14, 37, 'Dog Walking', -29, 2, 'COMPLETED', Decimal('840.00')),
            (17, 15, 40, 'Grooming & Bath', -17, 1, 'COMPLETED', Decimal('680.00')),
            (18, 16, 42, 'Dog Walking', -13, 2, 'COMPLETED', Decimal('560.00')),
            (19, 17, 44, 'Overnight Boarding', -27, 4, 'COMPLETED', Decimal('2320.00')),
            (0, 18, 0, 'Dog Walking', -8, 1, 'COMPLETED', Decimal('800.00')),
            (1, 19, 4, 'Pet Sitting', -9, 2, 'COMPLETED', Decimal('920.00')),
            (2, 0, 6, 'Dog Walking', -6, 1, 'COMPLETED', Decimal('500.00')),
            (3, 1, 9, 'Pet Sitting', -7, 2, 'COMPLETED', Decimal('1300.00')),

            (0, 0, 0, 'Dog Walking', 3, 2, 'ACCEPTED', Decimal('1000.00')),
            (1, 1, 3, 'Overnight Boarding', 5, 3, 'ACCEPTED', Decimal('1950.00')),
            (2, 2, 5, 'Daycare', 2, 1, 'ACCEPTED', Decimal('450.00')),
            (4, 3, 11, 'Pet Sitting', 4, 2, 'ACCEPTED', Decimal('1100.00')),
            (5, 5, 13, 'Grooming & Bath', 6, 1, 'ACCEPTED', Decimal('700.00')),
            (7, 7, 17, 'Daycare', 3, 2, 'ACCEPTED', Decimal('960.00')),
            (8, 8, 19, 'Pet Sitting', 5, 3, 'ACCEPTED', Decimal('2250.00')),

            (9, 9, 22, 'Dog Walking', 7, 2, 'PENDING', Decimal('760.00')),
            (10, 10, 24, 'Pet Sitting', 8, 3, 'PENDING', Decimal('1560.00')),
            (12, 12, 28, 'Pet Sitting', 10, 2, 'PENDING', Decimal('600.00')),
            (14, 14, 33, 'Dog Walking', 9, 1, 'PENDING', Decimal('420.00')),
            (16, 16, 37, 'Dog Walking', 11, 2, 'PENDING', Decimal('560.00')),

            (17, 17, 40, 'Overnight Boarding', -5, 2, 'CANCELLED', Decimal('1160.00')),
            (18, 18, 42, 'Dog Walking', -4, 1, 'CANCELLED', Decimal('800.00')),
            (19, 19, 44, 'Pet Sitting', -3, 2, 'REJECTED', Decimal('920.00')),
        ]

        created_bookings = []
        for c_idx, ct_idx, p_idx, srv, offset, duration, status, price in bookings_blueprint:
            owner = customers[c_idx]
            caretaker = caretakers[ct_idx]
            pet = pets[p_idx]
            s_date = today + timedelta(days=offset)
            e_date = s_date + timedelta(days=duration - 1)

            booking, _ = Booking.objects.get_or_create(
                owner=owner,
                caretaker=caretaker,
                pet=pet,
                start_date=s_date,
                defaults={
                    'end_date': e_date,
                    'service_type': srv,
                    'total_price': price,
                    'status': status,
                    'start_time': '09:00 AM',
                    'end_time': '05:00 PM',
                    'notes': f'Demo booking for {pet.name} with {caretaker.user.first_name}.',
                }
            )
            booking.end_date = e_date
            booking.service_type = srv
            booking.total_price = price
            booking.status = status
            booking.save()
            created_bookings.append(booking)

        return created_bookings

    def seed_reviews(self, bookings):
        self.stdout.write('Seeding Reviews for Completed Bookings...')
        completed = [b for b in bookings if b.status == 'COMPLETED']
        
        review_comments = [
            (5, 'Exceptional care! My pet was extremely happy and relaxed upon return. Highly recommended!'),
            (5, 'Very punctual, caring, and communicative with constant photo updates. Will book again!'),
            (4, 'Great sitter, followed all feeding and walking instructions carefully.'),
            (5, 'Outstanding service! Treated my pet like family. Could not ask for better care.'),
            (4, 'Very knowledgeable and gentle with large energetic dogs. Excellent experience.'),
            (5, 'Super responsive and attentive to medical schedules. Top-tier caretaker!'),
            (5, 'My cat adored her! Clean, stress-free environment and regular grooming.'),
            (4, 'Punctual and reliable for daily walking sessions. Very satisfied.'),
            (5, 'The best pet sitting experience in Tamil Nadu. 5 stars all the way!'),
            (4, 'Warm and welcoming family environment. Our dog loved the open play yard.'),
            (5, 'Professional, certified, and incredibly kind. Took great care of Bruno.'),
            (5, 'Detailed daily reports and GPS walk tracking were fantastic.'),
            (4, 'Friendly caretaker who easily handled our energetic pup.'),
            (5, 'Wonderful overnight boarding. Pet came home clean, energized, and happy!'),
            (4, 'Reliable and trustworthy. Handled medication flawlessly.'),
        ]

        created_reviews = []
        for i, b in enumerate(completed):
            rating, comment = review_comments[i % len(review_comments)]
            review, _ = Review.objects.get_or_create(
                booking=b,
                defaults={
                    'reviewer': b.owner,
                    'caretaker': b.caretaker,
                    'rating': rating,
                    'comment': f'{comment} ({b.pet.name} was so happy with {b.caretaker.user.first_name}!)',
                }
            )
            review.rating = rating
            review.comment = f'{comment} ({b.pet.name} was so happy with {b.caretaker.user.first_name}!)'
            review.save()
            created_reviews.append(review)

        for ct in set(b.caretaker for b in completed):
            ct.update_rating()

        return created_reviews

    def seed_health_data(self, pets):
        self.stdout.write('Seeding Pet Health Records, Vaccinations & Reminders...')
        today = timezone.now().date()
        count = 0

        for i, pet in enumerate(pets):
            if pet.species == 'Dog':
                vax_list = [
                    ('Rabies (Annual Booster)', -180, 185, 'BATCH-RB-9921', 'Dr. S. Sundaram BVSc', 'Madurai Pet Poly Clinic'),
                    ('DHPP 5-in-1 Core Vaccine', -240, 125, 'BATCH-DH-4410', 'Dr. V. Arulraj BVSc', 'Chennai Veterinary Hospital'),
                    ('Bordetella (Kennel Cough)', -300, 65, 'BATCH-BD-1123', 'Dr. K. Jayanthi BVSc', 'Coimbatore Animal Medical Center'),
                ]
            elif pet.species == 'Cat':
                vax_list = [
                    ('FVRCP 3-in-1 Feline Core', -210, 155, 'BATCH-FV-3321', 'Dr. R. Meena BVSc', 'Trichy Feline Care Clinic'),
                    ('Feline Rabies Vaccine', -320, 45, 'BATCH-FR-8812', 'Dr. S. Sundaram BVSc', 'Madurai Pet Poly Clinic'),
                ]
            else:
                vax_list = [
                    ('Exotic Companion Health Booster', -150, 215, 'BATCH-EX-1011', 'Dr. M. Deepan BVSc', 'Salem Exotic Pet Hospital'),
                ]

            for v_name, adm_offset, due_offset, batch, vet, clinic in vax_list:
                if pet.vaccination_status == 'Overdue':
                    due_offset = -15
                elif pet.vaccination_status == 'Due Soon':
                    due_offset = 4

                vax, _ = VaccinationRecord.objects.get_or_create(
                    pet=pet,
                    vaccine_name=v_name,
                    defaults={
                        'administered_date': today + timedelta(days=adm_offset),
                        'next_due_date': today + timedelta(days=due_offset),
                        'batch_number': batch,
                        'vet_name': vet,
                    }
                )
                vax.administered_date = today + timedelta(days=adm_offset)
                vax.next_due_date = today + timedelta(days=due_offset)
                vax.save()
                count += 1

            hrec, _ = HealthRecord.objects.get_or_create(
                pet=pet,
                condition_title='Annual Comprehensive Wellness Exam',
                defaults={
                    'record_date': today - timedelta(days=60),
                    'diagnosis': f'Overall physiological parameters within normal limits. {pet.name} is bright, alert, and responsive.',
                    'treatment_plan': 'Continue balanced diet, preventive monthly parasite control, and daily exercise.',
                    'vet_name': 'Dr. S. Sundaram BVSc',
                    'clinic_name': 'Tamil Nadu Pet Healthcare Hospital',
                }
            )
            count += 1

            if i % 3 == 0:
                med, _ = MedicineRecord.objects.get_or_create(
                    pet=pet,
                    medicine_name='NexGard Spectra Chewables',
                    defaults={
                        'dosage': '1 Chewable Tablet (Monthly)',
                        'frequency': 'Once every 30 days with food',
                        'start_date': today - timedelta(days=15),
                        'end_date': today + timedelta(days=165),
                        'notes': 'Broad spectrum flea, tick, and heartworm prevention.',
                        'is_active': True,
                    }
                )
                count += 1

            from health.weight_analytics import generate_realistic_weight_history_for_pet
            w_created = generate_realistic_weight_history_for_pet(pet)
            count += w_created

            if pet.allergies and pet.allergies.lower() != 'none':
                alg, _ = AllergyRecord.objects.get_or_create(
                    pet=pet,
                    allergy_name=pet.allergies,
                    defaults={
                        'severity': 'Moderate',
                        'notes': f'Prevent exposure to {pet.allergies}. Administer antihistamine under vet guidance if reaction occurs.'
                    }
                )
                count += 1

        return count

    def seed_lostfound_data(self, customers):
        self.stdout.write('Seeding Lost & Found Pet Reports, Police CSRs & Sightings...')
        from lostfound.models import LostPetReport, LostPetSighting
        import shutil

        today = timezone.now().date()
        owner = customers[0] if customers else User.objects.first()

        LostPetReport.objects.all().delete()

        r1 = LostPetReport.objects.create(
            reporter=owner,
            pet_name='Bruno',
            species='Dog',
            breed='Golden Retriever',
            gender='Male',
            approx_age='3.0 years',
            color_pattern='Rich Honey Golden coat with white star blaze on chest',
            distinctive_marks='Distinctive heart-shaped dark birthmark on inner left thigh, black spot on upper roof of mouth/tongue, docked tail, minor scar on right ear tip.',
            collar_description='Red reflective nylon collar with metal bell & engraved brass nametag "BRUNO"',
            microchip_id='981098102345678',
            last_seen_location='Besant Nagar Beach Promenade near 5th Avenue, Chennai, Tamil Nadu',
            date_lost=today - timedelta(days=3),
            time_lost='06:30 PM (Evening Walk)',
            how_lost='Startled by sudden loud festival firecrackers near beach car parking; slipped leash and sprinted towards 4th Main Road.',
            description='Extremely friendly, responds to whistle and the name "Bruno". Loves peanut butter treats. May be slightly anxious near heavy traffic.',
            police_complaint_status='FILED',
            police_station_name='J-2 Adyar Police Station, Chennai',
            police_csr_number='CSR No. 442/2026',
            police_filing_date=today - timedelta(days=2),
            police_contact_details='Sub-Inspector V. Ramanathan (044-2491-XXXX / Desk: 044-2491-2345)',
            reward_amount=Decimal('10000.00'),
            reward_details='₹10,000 Cash Reward - Guaranteed immediate payout upon safe return, no questions asked!',
            contact_name='Rajesh Kumar (Owner)',
            contact_number='+91 98401 23456',
            alternate_contact='+91 94440 98765 (Family)',
            status='SIGHTING_REPORTED'
        )

        LostPetSighting.objects.create(
            lost_pet=r1,
            reporter_name='Ananya Sundaram',
            reporter_contact='+91 98411 22334',
            sighting_location='Near Thalappakatti Restaurant, 2nd Avenue Besant Nagar',
            sighting_date=today - timedelta(days=2),
            sighting_time='08:15 PM',
            description='Saw a golden retriever matching Bruno with red collar heading towards the beach road. Looked thirsty, drank water from a puddle.'
        )

        LostPetSighting.objects.create(
            lost_pet=r1,
            reporter_name='Karthik Murugan',
            reporter_contact='+91 97900 33445',
            sighting_location='Near Damodar Gardens Gate, Adyar',
            sighting_date=today - timedelta(days=1),
            sighting_time='07:30 AM',
            description='Spotted wandering near tea stall. Very gentle, wagged tail when called Bruno but walked towards shaded garden lane.'
        )

        r2 = LostPetReport.objects.create(
            reporter=customers[1] if len(customers) > 1 else owner,
            pet_name='Bella',
            species='Dog',
            breed='Beagle',
            gender='Female',
            approx_age='2.0 years',
            color_pattern='Classic Tri-Color (Black saddle, tan legs & face, white chest & tail tip)',
            distinctive_marks='Unique white clover-shaped patch on nape of neck, distinct freckled tan spots across snout, notched left ear tip.',
            collar_description='Purple floral patterned collar with silver bell and rubber GPS holder',
            microchip_id='985141002938475',
            last_seen_location='Anna Nagar Tower Park, Gate 3, 3rd Avenue, Chennai, Tamil Nadu',
            date_lost=today - timedelta(days=2),
            time_lost='07:00 AM (Morning Jog)',
            how_lost='Followed a squirrel scent trail into dense hedge bushes; slipped harness while owner was tying shoelace.',
            description='Very energetic and food motivated. Responds to clicker and high-pitched voice. May approach people holding snacks.',
            police_complaint_status='FILED',
            police_station_name='K-4 Anna Nagar Police Station, Chennai',
            police_csr_number='CSR No. 318/2026',
            police_filing_date=today - timedelta(days=2),
            police_contact_details='Head Constable M. Selvam (044-2621-XXXX)',
            reward_amount=Decimal('5000.00'),
            reward_details='₹5,000 Cash Reward for safe return or verified sighting lead!',
            contact_name='Priya Sridhar',
            contact_number='+91 98840 55667',
            alternate_contact='+91 97910 11223',
            status='LOST'
        )

        r3 = LostPetReport.objects.create(
            reporter=customers[2] if len(customers) > 2 else owner,
            pet_name='Simba',
            species='Cat',
            breed='Persian Cat',
            gender='Male',
            approx_age='2.5 years',
            color_pattern='Pure Snow White long fur, striking Heterochromia odd-eyes',
            distinctive_marks='Striking Odd Eyes (Left eye deep cobalt blue, Right eye golden amber), small pink heart-shaped birthmark on left front paw pad, fluffy bottle-brush tail.',
            collar_description='Blue velvet breakaway collar with brass fish charm',
            microchip_id='RFID-TN-CHE-998821',
            last_seen_location='River View Enclave, Kotturpuram, Chennai, Tamil Nadu',
            date_lost=today - timedelta(days=4),
            time_lost='09:15 PM (Night)',
            how_lost='Escaped through balcony sliding glass door accidentally left unlatched during rain shower; hopped down garden compound terrace.',
            description='Indoor-only cat, likely hiding in quiet dry corners, under cars, or behind stairwells. Requires special hypoallergenic renal diet.',
            police_complaint_status='UNDER_REVIEW',
            police_station_name='J-3 Guindy Police Station, Chennai',
            police_csr_number='Diary Entry #89 (CSR under verification)',
            police_filing_date=today - timedelta(days=3),
            police_contact_details='Station Duty Officer (044-2235-XXXX)',
            reward_amount=Decimal('7500.00'),
            reward_details='₹7,500 Cash Reward - Simba needs daily medical care, please help us find him!',
            contact_name='Deepa Chandran',
            contact_number='+91 98412 34567',
            alternate_contact='+91 98410 88990',
            status='LOST'
        )

        r4 = LostPetReport.objects.create(
            reporter=customers[3] if len(customers) > 3 else owner,
            pet_name='Thor',
            species='Dog',
            breed='German Shepherd',
            gender='Male',
            approx_age='3.5 years',
            color_pattern='Black & Rich Tan saddle coat with black facial mask',
            distinctive_marks='Tan diamond blaze mark above right brow, white patch under chin, distinctive double dewclaws on rear legs, strong athletic build.',
            collar_description='Black tactical nylon collar with heavy-duty steel ring',
            microchip_id='981098105554321',
            last_seen_location='Velachery Main Road near Phoenix Marketcity, Chennai, Tamil Nadu',
            date_lost=today - timedelta(days=9),
            time_lost='08:30 PM',
            how_lost='Jumped compound gate chasing stray cats after heavy thunderclap.',
            description='Command trained in English and Tamil (Sit, Stay, Come). Protective yet gentle with humans.',
            police_complaint_status='FILED',
            police_station_name='S-14 Velachery Police Station, Chennai',
            police_csr_number='CSR No. 512/2026 (Case Resolved)',
            police_filing_date=today - timedelta(days=8),
            police_contact_details='Sub-Inspector K. Murugesan (044-2244-XXXX)',
            reward_amount=Decimal('15000.00'),
            reward_details='₹15,000 Cash Reward (Rewarded to MRTS security staff)',
            contact_name='Vikram Seth',
            contact_number='+91 99620 12345',
            alternate_contact='+91 98400 67890',
            status='REUNITED',
            reunited_date=today - timedelta(days=5),
            reunited_details='Safely recovered after an observant security guard at Velachery MRTS station recognized Thor from our Pet Care Companion lost alert! The guard sheltered him overnight and contacted us. Thor was reunited with his overjoyed family without a scratch!'
        )

        r5 = LostPetReport.objects.create(
            reporter=customers[4] if len(customers) > 4 else owner,
            pet_name='Milo (Found Pet)',
            species='Dog',
            breed='Indie / Indian Pariah Dog',
            gender='Male',
            approx_age='1.5 years',
            color_pattern='Fawn tan coat with black muzzle and white chest star',
            distinctive_marks='Curled sickle tail with bright white tip, distinct dark circular birthmark behind right ear, very clean and friendly (clearly someone\'s beloved pet).',
            collar_description='Green canvas collar without nametag (collar worn recently)',
            microchip_id='No microchip detected during vet scan',
            last_seen_location='Found near Pondy Bazaar Pedestrian Plaza, T. Nagar, Chennai, Tamil Nadu',
            date_lost=today - timedelta(days=1),
            time_lost='04:00 PM (Afternoon)',
            how_lost='Found wandering confused near street vendors in busy traffic. Rescued and currently sheltered safely at foster home in T. Nagar. Looking for original owner!',
            description='Extremely well-behaved, knows "shake hand" and "sit". Friendly with children and other dogs.',
            police_complaint_status='NOT_FILED',
            police_station_name='Blue Cross of India & Local T. Nagar Community Notice Filed',
            police_csr_number='Community Sighting Alert #TN-091',
            reward_amount=Decimal('0.00'),
            reward_details='No reward needed - Free handover upon showing pet ownership proof/photos',
            contact_name='Sneha Sundaram (Animal Rescuer / Foster)',
            contact_number='+91 98409 88776',
            alternate_contact='+91 99401 55443',
            status='FOUND'
        )

        r6 = LostPetReport.objects.create(
            reporter=customers[5] if len(customers) > 5 else owner,
            pet_name='Luna',
            species='Dog',
            breed='Siberian Husky',
            gender='Female',
            approx_age='2.5 years',
            color_pattern='Silver Grey and Snow White plush coat, Ice Blue Eyes',
            distinctive_marks='Symmetrical butterfly facial mask, distinctive black nose with pink "snow nose" center streak, tiny notch on tip of left ear, very striking blue eyes.',
            collar_description='Pink braided waterproof collar with stainless steel cylinder tag',
            microchip_id='981098776655443',
            last_seen_location='Race Course Walking Track / Redfields, Coimbatore, Tamil Nadu',
            date_lost=today - timedelta(days=1),
            time_lost='05:45 PM (Evening Walk)',
            how_lost='Slipped through automated sliding gate when delivery van entered compound; ran towards Race Course walking promenade.',
            description='Very vocal, howls when hearing sirens. Friendly but energetic. Cannot tolerate hot sun; urgent search underway!',
            police_complaint_status='FILED',
            police_station_name='B-4 Race Course Police Station, Coimbatore',
            police_csr_number='CSR No. 209/2026',
            police_filing_date=today,
            police_contact_details='Inspector S. Palanisamy (0422-222-XXXX)',
            reward_amount=Decimal('12000.00'),
            reward_details='₹12,000 Cash Reward for safe return or direct information leading to recovery!',
            contact_name='Dr. Arvind Balaji',
            contact_number='+91 94433 11223',
            alternate_contact='+91 98422 44556',
            status='LOST'
        )

        # Copy photos
        import os
        from django.conf import settings
        lost_dir = os.path.join(settings.MEDIA_ROOT, 'lost_pets')
        os.makedirs(lost_dir, exist_ok=True)

        photo_map = {
            r1: 'pets/pet_001.jpg',
            r2: 'pets/pet_006.jpg',
            r3: 'pets/pet_002.jpg',
            r4: 'pets/pet_004.jpg',
            r5: 'pets/pet_005.jpg',
            r6: 'pets/pet_003.jpg',
        }

        for rep_obj, src_rel in photo_map.items():
            src_path = os.path.join(settings.MEDIA_ROOT, src_rel)
            if os.path.exists(src_path):
                clean_name = rep_obj.pet_name.lower().split(' ')[0]
                dst_filename = f"lost_{clean_name}_{rep_obj.id}.jpg"
                dst_path = os.path.join(lost_dir, dst_filename)
                shutil.copyfile(src_path, dst_path)
                rep_obj.photo = f"lost_pets/{dst_filename}"
                rep_obj.save(update_fields=['photo'])

        return LostPetReport.objects.count()


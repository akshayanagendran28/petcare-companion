import os
import sys
import django
from decimal import Decimal
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from lostfound.models import LostPetReport, LostPetSighting

User = get_user_model()
owner = User.objects.filter(role='PET_OWNER').first()
if not owner:
    owner = User.objects.filter(is_superuser=True).first()

today = timezone.now().date()

# Clear existing
LostPetReport.objects.all().delete()

# 1. Bruno (Golden Retriever - LOST / Sighting Reported)
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

# 2. Bella (Beagle - LOST)
r2 = LostPetReport.objects.create(
    reporter=owner,
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

LostPetSighting.objects.create(
    lost_pet=r2,
    reporter_name='Vignesh Parthasarathy',
    reporter_contact='+91 98844 99887',
    sighting_location='Near Shanthi Colony Roundabout, Anna Nagar',
    sighting_date=today - timedelta(days=1),
    sighting_time='06:45 PM',
    description='Saw a small tri-color beagle with purple collar sniffing near juice shop. Ran towards 4th avenue when a scooter honked.'
)

# 3. Simba (Persian Cat - LOST)
r3 = LostPetReport.objects.create(
    reporter=owner,
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

# 4. Thor (German Shepherd - REUNITED)
r4 = LostPetReport.objects.create(
    reporter=owner,
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

# 5. Milo (Indie Dog - FOUND by Rescuer)
r5 = LostPetReport.objects.create(
    reporter=owner,
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

# 6. Luna (Siberian Husky - LOST)
r6 = LostPetReport.objects.create(
    reporter=owner,
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

# Assign photos
import shutil
lost_dir = os.path.join(BASE_DIR, 'media', 'lost_pets')
os.makedirs(lost_dir, exist_ok=True)

photo_map = {
    r1: 'media/pets/pet_001.jpg',
    r2: 'media/pets/pet_006.jpg',
    r3: 'media/pets/pet_002.jpg',
    r4: 'media/pets/pet_004.jpg',
    r5: 'media/pets/pet_005.jpg',
    r6: 'media/pets/pet_003.jpg',
}

for rep_obj, src_rel in photo_map.items():
    src_path = os.path.join(BASE_DIR, src_rel)
    if os.path.exists(src_path):
        clean_name = rep_obj.pet_name.lower().split(' ')[0]
        dst_filename = f"lost_{clean_name}_{rep_obj.id}.jpg"
        dst_path = os.path.join(lost_dir, dst_filename)
        shutil.copyfile(src_path, dst_path)
        rep_obj.photo = f"lost_pets/{dst_filename}"
        rep_obj.save(update_fields=['photo'])

# Generate Police CSR Documents & Run ML Document Verification
from lostfound.document_verifier import generate_sample_police_csr_document, verify_police_document_ml
import json

docs_dir = os.path.join(BASE_DIR, 'media', 'police_docs')
os.makedirs(docs_dir, exist_ok=True)

for rep in LostPetReport.objects.all():
    if rep.police_complaint_status in ['FILED', 'UNDER_REVIEW']:
        clean_name = rep.pet_name.lower().split(' ')[0]
        doc_filename = f"police_csr_{clean_name}_{rep.id}.jpg"
        doc_path = os.path.join(docs_dir, doc_filename)
        generate_sample_police_csr_document(rep, doc_path)
        rep.police_document = f"police_docs/{doc_filename}"
        
        meta = {
            'pet_name': rep.pet_name,
            'species': rep.species,
            'breed': rep.breed,
            'contact_name': rep.contact_name,
            'police_csr_number': rep.police_csr_number,
            'police_station_name': rep.police_station_name,
            'date_lost': rep.date_lost
        }
        res = verify_police_document_ml(doc_path, meta)
        
        rep.police_verified_by_ai = res['is_valid']
        rep.police_verification_confidence = Decimal(str(res['confidence']))
        rep.police_verification_details = json.dumps(res['breakdown'])
        rep.police_verified_at = timezone.now()
        if res['is_valid']:
            rep.police_complaint_status = 'FILED'
        rep.save()

print(f"Successfully seeded {LostPetReport.objects.count()} comprehensive Lost & Found pet records with photos and ML verified police CSR copies!")



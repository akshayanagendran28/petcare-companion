import hashlib
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# Comprehensive Breed Weight Benchmarks (kg)
BREED_WEIGHT_RANGES = {
    # Dogs
    ('dog', 'labrador retriever'): (25.0, 34.0, 'Labrador Retriever'),
    ('dog', 'labrador'): (25.0, 34.0, 'Labrador Retriever'),
    ('dog', 'golden retriever'): (25.0, 34.0, 'Golden Retriever'),
    ('dog', 'german shepherd'): (30.0, 40.0, 'German Shepherd'),
    ('dog', 'beagle'): (9.0, 13.5, 'Beagle'),
    ('dog', 'french bulldog'): (8.0, 12.5, 'French Bulldog'),
    ('dog', 'bulldog'): (18.0, 25.0, 'Bulldog'),
    ('dog', 'poodle'): (6.0, 12.0, 'Poodle'),
    ('dog', 'standard poodle'): (20.0, 32.0, 'Standard Poodle'),
    ('dog', 'miniature poodle'): (4.5, 7.5, 'Miniature Poodle'),
    ('dog', 'toy poodle'): (2.0, 4.0, 'Toy Poodle'),
    ('dog', 'rottweiler'): (35.0, 50.0, 'Rottweiler'),
    ('dog', 'boxer'): (25.0, 32.0, 'Boxer'),
    ('dog', 'siberian husky'): (16.0, 27.0, 'Siberian Husky'),
    ('dog', 'husky'): (16.0, 27.0, 'Siberian Husky'),
    ('dog', 'dachshund'): (5.0, 9.5, 'Dachshund'),
    ('dog', 'great dane'): (50.0, 80.0, 'Great Dane'),
    ('dog', 'doberman pinscher'): (32.0, 45.0, 'Doberman Pinscher'),
    ('dog', 'doberman'): (32.0, 45.0, 'Doberman Pinscher'),
    ('dog', 'shih tzu'): (4.0, 7.5, 'Shih Tzu'),
    ('dog', 'pug'): (6.0, 8.5, 'Pug'),
    ('dog', 'chihuahua'): (1.2, 3.0, 'Chihuahua'),
    ('dog', 'pomeranian'): (1.5, 3.5, 'Pomeranian'),
    ('dog', 'border collie'): (14.0, 20.0, 'Border Collie'),
    ('dog', 'cavalier king charles spaniel'): (5.5, 8.5, 'Cavalier King Charles'),
    ('dog', 'cocker spaniel'): (11.0, 15.0, 'Cocker Spaniel'),
    ('dog', 'english cocker spaniel'): (12.0, 15.5, 'English Cocker Spaniel'),
    ('dog', 'english setter'): (20.0, 30.0, 'English Setter'),
    ('dog', 'havanese'): (3.5, 6.0, 'Havanese'),
    ('dog', 'japanese chin'): (2.0, 4.5, 'Japanese Chin'),
    ('dog', 'keeshond'): (15.0, 20.0, 'Keeshond'),
    ('dog', 'leonberger'): (45.0, 75.0, 'Leonberger'),
    ('dog', 'miniature pinscher'): (3.5, 5.0, 'Miniature Pinscher'),
    ('dog', 'newfoundland'): (50.0, 70.0, 'Newfoundland'),
    ('dog', 'saint bernard'): (60.0, 90.0, 'Saint Bernard'),
    ('dog', 'samoyed'): (20.0, 30.0, 'Samoyed'),
    ('dog', 'scottish terrier'): (8.5, 10.5, 'Scottish Terrier'),
    ('dog', 'staffordshire bull terrier'): (13.0, 17.5, 'Staffordshire Bull Terrier'),
    ('dog', 'wheaten terrier'): (14.0, 18.5, 'Wheaten Terrier'),
    ('dog', 'yorkshire terrier'): (2.0, 3.5, 'Yorkshire Terrier'),
    ('dog', 'indie'): (14.0, 22.0, 'Indie Dog'),
    ('dog', 'indian pariah dog'): (14.0, 22.0, 'Indian Pariah Dog'),
    ('dog', 'mixed breed'): (12.0, 24.0, 'Mixed Breed'),
    
    # Cats
    ('cat', 'persian'): (3.5, 5.5, 'Persian Cat'),
    ('cat', 'persian cat'): (3.5, 5.5, 'Persian Cat'),
    ('cat', 'siamese'): (3.0, 4.8, 'Siamese Cat'),
    ('cat', 'maine coon'): (5.5, 9.5, 'Maine Coon'),
    ('cat', 'british shorthair'): (4.0, 7.5, 'British Shorthair'),
    ('cat', 'ragdoll'): (4.5, 8.5, 'Ragdoll'),
    ('cat', 'bengal'): (3.8, 6.8, 'Bengal Cat'),
    ('cat', 'sphynx'): (3.0, 5.0, 'Sphynx Cat'),
    ('cat', 'abyssinian'): (3.0, 4.5, 'Abyssinian'),
    ('cat', 'birman'): (3.5, 5.5, 'Birman'),
    ('cat', 'bombay'): (3.0, 5.0, 'Bombay Cat'),
    ('cat', 'bombay cat'): (3.0, 5.0, 'Bombay Cat'),
    ('cat', 'egyptian mau'): (3.0, 5.0, 'Egyptian Mau'),
    ('cat', 'russian blue'): (3.5, 5.5, 'Russian Blue'),
    ('cat', 'norwegian forest cat'): (4.5, 8.0, 'Norwegian Forest Cat'),
    ('cat', 'scottish fold'): (3.0, 6.0, 'Scottish Fold'),
    ('cat', 'domestic shorthair'): (3.5, 5.5, 'Domestic Shorthair'),
    ('cat', 'indie'): (3.2, 5.2, 'Domestic Cat'),
    
    # Birds
    ('bird', 'african grey'): (0.38, 0.55, 'African Grey'),
    ('bird', 'cockatiel'): (0.08, 0.12, 'Cockatiel'),
    ('bird', 'budgerigar'): (0.03, 0.045, 'Budgerigar'),
    ('bird', 'budgie'): (0.03, 0.045, 'Budgie'),
    ('bird', 'parakeet'): (0.03, 0.05, 'Parakeet'),
    ('bird', 'lovebird'): (0.04, 0.06, 'Lovebird'),
    ('bird', 'amazon parrot'): (0.35, 0.55, 'Amazon Parrot'),
    ('bird', 'macaw'): (0.9, 1.5, 'Macaw'),
    ('bird', 'cockatoo'): (0.4, 0.8, 'Cockatoo'),
    ('bird', 'conure'): (0.08, 0.15, 'Conure'),
    ('bird', 'finch'): (0.015, 0.025, 'Finch'),
    ('bird', 'canary'): (0.02, 0.035, 'Canary'),

    # Rabbits
    ('rabbit', 'holland lop'): (1.4, 2.0, 'Holland Lop'),
    ('rabbit', 'netherland dwarf'): (0.8, 1.25, 'Netherland Dwarf'),
    ('rabbit', 'flemish giant'): (4.5, 7.5, 'Flemish Giant'),
    ('rabbit', 'mini rex'): (1.5, 2.2, 'Mini Rex'),
    ('rabbit', 'lionhead'): (1.3, 1.8, 'Lionhead'),
}


def get_breed_target_range(species, breed, current_weight=None):
    """
    Looks up ideal breed target weight range (min_kg, max_kg, label).
    Falls back gracefully if not explicitly indexed.
    """
    s = (species or 'dog').strip().lower()
    b = (breed or '').strip().lower()

    # Direct match
    if (s, b) in BREED_WEIGHT_RANGES:
        min_w, max_w, label = BREED_WEIGHT_RANGES[(s, b)]
        return {
            'min_kg': min_w,
            'max_kg': max_w,
            'label': f"{label} Target ({min_w} – {max_w} kg)",
            'short_label': f"{min_w} – {max_w} kg"
        }

    # Partial substring match
    for (spec_key, breed_key), (min_w, max_w, label) in BREED_WEIGHT_RANGES.items():
        if spec_key == s and (breed_key in b or b in breed_key):
            return {
                'min_kg': min_w,
                'max_kg': max_w,
                'label': f"{label} Target ({min_w} – {max_w} kg)",
                'short_label': f"{min_w} – {max_w} kg"
            }

    # Dynamic fallback based on current weight or species standard
    cur = float(current_weight or 15.0)
    if cur <= 0:
        cur = 10.0
    min_w = round(cur * 0.88, 1)
    max_w = round(cur * 1.12, 1)
    disp_name = breed.title() if breed else s.title()
    return {
        'min_kg': min_w,
        'max_kg': max_w,
        'label': f"{disp_name} Reference ({min_w} – {max_w} kg)",
        'short_label': f"{min_w} – {max_w} kg"
    }


def calculate_weight_status(current_weight, min_target, max_target):
    """Returns status badge and label based on ideal weight target."""
    if current_weight is None:
        return {'status': 'Unknown', 'color': 'secondary', 'icon': 'fa-circle-question'}
    
    w = float(current_weight)
    if w < min_target:
        diff = round(min_target - w, 1)
        return {
            'status': f'Under Target (-{diff} kg)',
            'short_status': 'Under Target',
            'color': 'warning',
            'badge_class': 'bg-warning text-dark',
            'icon': 'fa-triangle-exclamation'
        }
    elif w > max_target:
        diff = round(w - max_target, 1)
        return {
            'status': f'Above Target (+{diff} kg)',
            'short_status': 'Above Target',
            'color': 'danger',
            'badge_class': 'bg-danger text-white',
            'icon': 'fa-triangle-exclamation'
        }
    else:
        return {
            'status': 'Optimal Healthy Weight',
            'short_status': 'Optimal Target',
            'color': 'success',
            'badge_class': 'bg-success text-white',
            'icon': 'fa-circle-check'
        }


def generate_realistic_weight_history_for_pet(pet, num_points=7):
    """
    Generates 6-8 distinct, realistic historical weight check-in data points
    for a pet over the last 9-12 months.
    Uses deterministic pseudo-randomness based on pet attributes so each pet
    has a unique, sensible trajectory tailored to age, species, and breed.
    """
    from .models import WeightRecord

    target_weight = float(pet.weight or 15.0)
    age = float(pet.age or 2.0)
    today = timezone.now().date()

    # Seed RNG deterministically for this pet
    seed_str = f"pet_weight_{pet.id}_{pet.name}_{pet.breed}_{target_weight}"
    seed_int = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest()[:8], 16)
    rng = random.Random(seed_int)

    # Days intervals going back in time
    day_offsets = [330, 270, 210, 150, 90, 30, 0]
    if num_points == 8:
        day_offsets = [360, 300, 240, 180, 120, 60, 15, 0]

    checkup_notes = [
        "Annual comprehensive wellness check & baseline",
        "Quarterly weight & body condition score check",
        "Mid-year preventive care & booster weigh-in",
        "Routine checkup & diet evaluation",
        "Grooming visit weigh-in & health check",
        "Pre-seasonal wellness examination",
        "Recent checkup & routine weigh-in",
        "Current weight check"
    ]

    records_to_create = []

    # Growth curve calculation
    for idx, days_ago in enumerate(day_offsets):
        record_date = today - timedelta(days=days_ago + rng.randint(-3, 3))
        note = checkup_notes[idx % len(checkup_notes)]

        if days_ago == 0:
            # Latest point matches current pet weight exactly
            val = target_weight
            note = "Current logged weight"
        else:
            progress = (len(day_offsets) - 1 - idx) / float(len(day_offsets) - 1)
            
            if age <= 1.0:
                # Puppy / Kitten: rapid growth curve (starts around 50-70% of current weight)
                factor = 0.55 + (0.45 * progress) + (rng.uniform(-0.03, 0.03))
                val = max(0.1, target_weight * factor)
            elif age <= 2.0:
                # Young Pet: slight growth / filling out (starts around 85-90% of current weight)
                factor = 0.88 + (0.12 * progress) + (rng.uniform(-0.02, 0.02))
                val = max(0.1, target_weight * factor)
            elif age >= 8.0:
                # Senior Pet: very stable maintenance with minor seasonal drift
                variation = rng.uniform(-0.03, 0.03) * target_weight
                val = max(0.1, target_weight + variation)
            else:
                # Adult Pet: subtle realistic variations (+/- 3-6%) across seasons
                # Introduce a slight curve (e.g. slight winter weight or post-exercise fitness)
                seasonal_wave = 0.03 * target_weight * ((idx % 3) - 1)
                random_noise = rng.uniform(-0.02, 0.02) * target_weight
                val = max(0.1, target_weight + seasonal_wave + random_noise)

            # Round appropriately
            if target_weight < 1.0:
                val = round(val, 3)
            elif target_weight < 5.0:
                val = round(val, 2)
            else:
                val = round(val, 1)

        records_to_create.append(
            WeightRecord(
                pet=pet,
                recorded_date=record_date,
                weight_kg=Decimal(str(val)),
                notes=note
            )
        )

    # Replace existing weight history for this pet with the realistic timeline
    WeightRecord.objects.filter(pet=pet).delete()
    WeightRecord.objects.bulk_create(records_to_create)
    return len(records_to_create)

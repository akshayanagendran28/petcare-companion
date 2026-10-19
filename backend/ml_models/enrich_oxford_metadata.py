import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_PATH = os.path.join(BASE_DIR, 'ml_models', 'breed_metadata.json')

with open(METADATA_PATH, 'r', encoding='utf-8') as f:
    meta = json.load(f)

oxford_profiles = {
    'Abyssinian': {
        'species': 'Cat',
        'group': 'Shorthair / Ancient Feline',
        'origin': 'Ethiopia / Egypt',
        'lifespan': '13 - 16 years',
        'weight_range': '3.0 - 5.0 kg',
        'temperament': ['Curious', 'Highly Intelligent', 'Agile', 'Playful', 'Affectionate'],
        'exercise_needs': 'High (Loves vertical perches, climbing trees, and puzzle games)',
        'grooming_needs': 'Low (Short ticked warm coat, weekly brushing)',
        'diet_guide': 'High-protein feline diet rich in taurine to support lean, muscular athleticism.',
        'ideal_caretaker': 'Active owners who appreciate an energetic, clownish, and inquisitive feline friend.',
        'care_tips': 'Needs mental stimulation. Provide multi-level cat trees and interactive wand toys.'
    },
    'American Bulldog': {
        'species': 'Dog',
        'group': 'Working / Molosser Group',
        'origin': 'United States',
        'lifespan': '10 - 12 years',
        'weight_range': '30 - 50 kg',
        'temperament': ['Confident', 'Loyal', 'Energetic', 'Protective', 'Affectionate'],
        'exercise_needs': 'High (60 mins daily walks and strength games)',
        'grooming_needs': 'Low (Short smooth coat, weekly brushing)',
        'diet_guide': 'Large-breed muscular formula with joint-protecting glucosamine and chondroitin.',
        'ideal_caretaker': 'Confident, experienced dog owners who provide consistent positive training.',
        'care_tips': 'Requires early socialization. Clean skin folds and keep nails trimmed.'
    },
    'American Pit Bull Terrier': {
        'species': 'Dog',
        'group': 'Terrier Group',
        'origin': 'United States',
        'lifespan': '12 - 14 years',
        'weight_range': '15 - 28 kg',
        'temperament': ['Deeply Loyal', 'Affectionate with Family', 'Courageous', 'Playful', 'Eager to please'],
        'exercise_needs': 'High (60-90 mins athletic workouts, agility, hiking)',
        'grooming_needs': 'Low (Short single coat, quick wipe-down)',
        'diet_guide': 'High-protein diet supporting lean muscle mass and healthy skin.',
        'ideal_caretaker': 'Dedicated pet owners who provide lots of love, structure, and athletic play.',
        'care_tips': 'Thrives on positive reinforcement training. Loves soft bedding and cuddle time.'
    },
    'Birman': {
        'species': 'Cat',
        'group': 'Semi-Longhair Group (The Sacred Cat of Burma)',
        'origin': 'Burma / France',
        'lifespan': '13 - 16 years',
        'weight_range': '3.5 - 6.0 kg',
        'temperament': ['Gentle', 'Quiet', 'Loving', 'Docile', 'Companionable'],
        'exercise_needs': 'Low to Moderate (Gentle floor play and feather chase)',
        'grooming_needs': 'Moderate (Silky coat with little undercoat, does not mat easily)',
        'diet_guide': 'Balanced indoor feline diet with omega-3 fatty acids for lustrous coat.',
        'ideal_caretaker': 'Peaceful households looking for a sweet-natured lap cat with distinct white paws.',
        'care_tips': 'Famous for distinct sapphire blue eyes and pure white gloves on all four paws.'
    },
    'Bombay': {
        'species': 'Cat',
        'group': 'Shorthair Group (The Mini Black Panther)',
        'origin': 'United States',
        'lifespan': '14 - 18 years',
        'weight_range': '3.5 - 5.5 kg',
        'temperament': ['Outgoing', 'Affectionate', 'Curious', 'Warm-seeking', 'Playful'],
        'exercise_needs': 'Moderate (Interactive chasing toys and warm lap snuggles)',
        'grooming_needs': 'Low (Sleek patent-leather black coat, weekly rubber brush)',
        'diet_guide': 'Premium protein wet and dry food; monitor portions as they love eating.',
        'ideal_caretaker': 'Owners who love an attentive, velvety black cat that follows them everywhere.',
        'care_tips': 'Loves seeking out warm sunbeams and cozy blankets. Very social.'
    },
    'Great Pyrenees': {
        'species': 'Dog',
        'group': 'Livestock Guardian / Working',
        'origin': 'Pyrenees Mountains (France/Spain)',
        'lifespan': '10 - 12 years',
        'weight_range': '40 - 55 kg',
        'temperament': ['Calm', 'Patient', 'Fearless Guardian', 'Gentle Giant', 'Independent'],
        'exercise_needs': 'Moderate (30-45 mins calm walking and perimeter patrol)',
        'grooming_needs': 'High (Thick weather-resistant white double coat, regular brushing)',
        'diet_guide': 'Giant-breed growth formula with controlled calcium/phosphorus ratios.',
        'ideal_caretaker': 'Homes with spacious fenced yards; sitters experienced with gentle giant guardians.',
        'care_tips': 'Natural night guardians; ensure sturdy fencing as they love patrolling territory.'
    },
    'Havanese': {
        'species': 'Dog',
        'group': 'Toy Group / National Dog of Cuba',
        'origin': 'Cuba',
        'lifespan': '14 - 16 years',
        'weight_range': '3.5 - 6.0 kg',
        'temperament': ['Playful', 'Affectionate', 'Gentle', 'Charming', 'Social'],
        'exercise_needs': 'Moderate (30 mins daily walking and indoor games)',
        'grooming_needs': 'High (Long silky coat, daily brushing or puppy cut clipping)',
        'diet_guide': 'Small-breed nutrient-dense kibble designed for toy jaws.',
        'ideal_caretaker': 'Families and seniors looking for a Velcro companion dog.',
        'care_tips': 'Prone to separation anxiety; thrives when included in daily household activities.'
    },
    'Ragdoll': {
        'species': 'Cat',
        'group': 'Semi-Longhair Group',
        'origin': 'California, United States',
        'lifespan': '13 - 17 years',
        'weight_range': '4.5 - 9.0 kg',
        'temperament': ['Placid', 'Sweet', 'Affectionate', 'Puppy-like', 'Docile'],
        'exercise_needs': 'Low (Gentle indoor interactive play)',
        'grooming_needs': 'Moderate (Plush rabbit-soft coat, twice-weekly combing)',
        'diet_guide': 'Large-breed feline diet supporting slow muscular growth and coat luster.',
        'ideal_caretaker': 'Loving indoor households who want a super cuddly, relaxed lap feline.',
        'care_tips': 'Named for going limp like a ragdoll when held. Strictly indoor cat.'
    },
    'Russian Blue': {
        'species': 'Cat',
        'group': 'Shorthair Group',
        'origin': 'Arkhangelsk, Russia',
        'lifespan': '15 - 20 years',
        'weight_range': '3.5 - 5.5 kg',
        'temperament': ['Reserved', 'Intelligent', 'Gentle', 'Quiet', 'Deeply Loyal to family'],
        'exercise_needs': 'Moderate (Loves laser pointer chase and vertical wall climbs)',
        'grooming_needs': 'Low (Dense shimmering silver-tipped blue coat, weekly brushing)',
        'diet_guide': 'High-protein diet; monitor portions to prevent weight gain.',
        'ideal_caretaker': 'Calm, quiet homes who appreciate an elegant, low-allergen companion.',
        'care_tips': 'Famous for vivid emerald green eyes and plush double coat.'
    },
    'Saint Bernard': {
        'species': 'Dog',
        'group': 'Giant Working Group / Alpine Rescue',
        'origin': 'Swiss Alps (Switzerland/Italy)',
        'lifespan': '8 - 10 years',
        'weight_range': '60 - 85 kg',
        'temperament': ['Gentle', 'Friendly', 'Patient', 'Calm', 'Devoted'],
        'exercise_needs': 'Moderate (30-45 mins relaxed cool-weather walks)',
        'grooming_needs': 'Moderate to High (Heavy seasonal shedding, drool wiping)',
        'diet_guide': 'Giant-breed joint-support formula with controlled caloric intake.',
        'ideal_caretaker': 'Families with spacious ground-floor homes capable of handling giant breeds.',
        'care_tips': 'Sensitive to hot weather; ensure air-conditioning and plenty of fresh cool water.'
    },
    'Shiba Inu': {
        'species': 'Dog',
        'group': 'Spitz Group / National Dog of Japan',
        'origin': 'Japan',
        'lifespan': '13 - 16 years',
        'weight_range': '8.0 - 11.5 kg',
        'temperament': ['Alert', 'Independent', 'Confident', 'Fastidious', 'Loyal'],
        'exercise_needs': 'Moderate to High (45-60 mins daily walks and agility)',
        'grooming_needs': 'Moderate (Clean cat-like self-groomers, seasonal coat blowouts)',
        'diet_guide': 'High-protein balanced kibble with omega-3 for thick double coat.',
        'ideal_caretaker': 'Experienced owners who appreciate an independent, dignified spitz breed.',
        'care_tips': 'Always walk on leash as they have strong prey drive. Famous for the Shiba scream.'
    },
    'Sphynx': {
        'species': 'Cat',
        'group': 'Hairless Group',
        'origin': 'Toronto, Canada',
        'lifespan': '12 - 15 years',
        'weight_range': '3.0 - 5.5 kg',
        'temperament': ['Extroverted', 'Warm-seeking', 'Cuddly', 'Playful', 'Curious'],
        'exercise_needs': 'Moderate to High (Very active, loves climbing and puzzle toys)',
        'grooming_needs': 'Specialized (Weekly gentle sponge baths to remove natural skin oils)',
        'diet_guide': 'High-calorie diet as hairless metabolism burns more energy staying warm.',
        'ideal_caretaker': 'Attentive owners who can provide weekly skin care and warm winter sweaters.',
        'care_tips': 'Must be protected from direct sunburn and winter drafts.'
    }
}

for k, v in oxford_profiles.items():
    meta[k] = v

with open(METADATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2)

print(f"Enriched breed metadata! Total breeds now: {len(meta)}")

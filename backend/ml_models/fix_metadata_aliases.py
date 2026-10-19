import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_PATH = os.path.join(BASE_DIR, 'ml_models', 'breed_metadata.json')
LABELS_PATH = os.path.join(BASE_DIR, 'ml_models', 'imagenet_labels.json')

with open(METADATA_PATH, 'r', encoding='utf-8') as f:
    meta = json.load(f)

with open(LABELS_PATH, 'r', encoding='utf-8') as f:
    labels = json.load(f)

# Core authentic profiles for Cats
cat_profiles = {
    'Egyptian Mau': {
        'species': 'Cat',
        'group': 'Spotted Shorthair / Ancient Feline',
        'origin': 'Egypt',
        'lifespan': '12 - 15 years',
        'weight_range': '3.0 - 5.0 kg',
        'temperament': ['Fast & Athletic', 'Intelligent', 'Loyal', 'Playful', 'Affectionate'],
        'exercise_needs': 'High (Extremely fast runner; loves vertical climbs and interactive feather wands)',
        'grooming_needs': 'Low (Short spotted coat, weekly brushing)',
        'diet_guide': 'High-protein feline formula with taurine and omega fatty acids for a shimmering spotted coat.',
        'ideal_caretaker': 'Active owners who appreciate a lively, loyal, and fast-moving ancient feline companion.',
        'care_tips': 'The only naturally spotted breed of domesticated cat; can run up to 48 km/h.'
    },
    'Persian': {
        'species': 'Cat',
        'group': 'Longhair Group',
        'origin': 'Iran (Persia)',
        'lifespan': '12 - 17 years',
        'weight_range': '3.5 - 5.5 kg',
        'temperament': ['Gentle', 'Quiet', 'Sweet-tempered', 'Placid', 'Affectionate'],
        'exercise_needs': 'Low (Calm indoor play and relaxing in cozy sunspots)',
        'grooming_needs': 'High (Daily combing to prevent mats, eye corner cleaning)',
        'diet_guide': 'Hairball-control high-protein diet with omega oils for a plush luxurious coat.',
        'ideal_caretaker': 'Serene, calm indoor households looking for a gentle, affectionate lap companion.',
        'care_tips': 'Requires daily coat grooming and gentle face wiping around nasal folds.'
    },
    'Siamese': {
        'species': 'Cat',
        'group': 'Oriental Shorthair Group',
        'origin': 'Thailand (Siam)',
        'lifespan': '14 - 20 years',
        'weight_range': '3.5 - 5.5 kg',
        'temperament': ['Vocal', 'Deeply Affectionate', 'Extroverted', 'Social', 'Intelligent'],
        'exercise_needs': 'Moderate to High (Loves interactive games, fetch, and conversational bonding)',
        'grooming_needs': 'Low (Sleek short fine coat, weekly brushing)',
        'diet_guide': 'Lean protein feline diet supporting active metabolism and slender body condition.',
        'ideal_caretaker': 'Families who enjoy an outgoing, highly talkative, and loving feline partner.',
        'care_tips': 'Deeply social; best in pairs or with owners who spend plenty of time at home.'
    },
    'Bengal': {
        'species': 'Cat',
        'group': 'Exotic Spotted / Marbled Shorthair',
        'origin': 'United States',
        'lifespan': '12 - 16 years',
        'weight_range': '4.5 - 7.5 kg',
        'temperament': ['Athletic', 'Curious', 'High Energy', 'Confident', 'Playful'],
        'exercise_needs': 'Very High (Enjoys cat exercise wheels, water play, and harness walking)',
        'grooming_needs': 'Low (Glittered pelt-like coat, weekly brushing)',
        'diet_guide': 'Nutrient-rich, high-protein diet supporting powerful muscular physique.',
        'ideal_caretaker': 'Energetic households ready to provide high vertical spaces and puzzle games.',
        'care_tips': 'Often loves playing with running water; requires ample mental and physical engagement.'
    },
    'Tabby': {
        'species': 'Cat',
        'group': 'Domestic Shorthair / Classic Tabby',
        'origin': 'Global / Domestic Feline',
        'lifespan': '13 - 18 years',
        'weight_range': '3.5 - 6.0 kg',
        'temperament': ['Friendly', 'Adaptable', 'Playful', 'Affectionate', 'Curious'],
        'exercise_needs': 'Moderate (Daily interactive play, laser pointer chase, scratching posts)',
        'grooming_needs': 'Low (Weekly brushing and nail trimming)',
        'diet_guide': 'Complete and balanced feline nutrition formulated for indoor life-stage health.',
        'ideal_caretaker': 'All loving pet households looking for a warm, cheerful, and adaptable companion.',
        'care_tips': 'Provide variety in toys, window perches for bird watching, and clean fresh water.'
    },
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
    'Birman': {
        'species': 'Cat',
        'group': 'Semi-Longhair (The Sacred Cat of Burma)',
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
    'British Shorthair': {
        'species': 'Cat',
        'group': 'Shorthair Group',
        'origin': 'Great Britain',
        'lifespan': '14 - 17 years',
        'weight_range': '4.0 - 7.5 kg',
        'temperament': ['Calm', 'Easygoing', 'Affectionate', 'Dignified', 'Patient'],
        'exercise_needs': 'Moderate (Enjoys feather chasing and short bursts of play)',
        'grooming_needs': 'Low (Plush dense coat, weekly brushing)',
        'diet_guide': 'Balanced indoor formula; monitor calories to maintain optimal body weight.',
        'ideal_caretaker': 'Families looking for a round-faced, placid, and undemanding companion.',
        'care_tips': 'The iconic teddy-bear cat with dense plush fur and copper eyes.'
    },
    'Maine Coon': {
        'species': 'Cat',
        'group': 'Giant Longhair Group',
        'origin': 'Maine, United States',
        'lifespan': '12 - 15 years',
        'weight_range': '5.5 - 10.0 kg',
        'temperament': ['Gentle Giant', 'Friendly', 'Playful', 'Intelligent', 'Dog-like'],
        'exercise_needs': 'Moderate to High (Large climbing structures, fetch games)',
        'grooming_needs': 'Moderate (Water-resistant heavy coat, twice-weekly brushing)',
        'diet_guide': 'Large-breed feline diet supporting healthy joints and massive bone frame.',
        'ideal_caretaker': 'Families looking for a large, gregarious, and affectionate cat.',
        'care_tips': 'One of the largest domesticated cat breeds; distinctive lynx-tipped ears and bushy tail.'
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

# Add cat profiles and both alias variations (e.g. 'Persian' and 'Persian Cat')
for k, v in cat_profiles.items():
    meta[k] = v
    if not k.endswith('Cat'):
        meta[f"{k} Cat"] = v
    else:
        base = k.replace(' Cat', '').strip()
        meta[base] = v

# Dog missing breeds
dog_profiles = {
    'Giant Schnauzer': {
        'species': 'Dog',
        'group': 'Working Group',
        'origin': 'Germany',
        'lifespan': '10 - 12 years',
        'weight_range': '30 - 45 kg',
        'temperament': ['Alert', 'Commanding', 'Loyal', 'Intelligent', 'Powerful'],
        'exercise_needs': 'High (60-90 mins daily strenuous exercise and mental training)',
        'grooming_needs': 'High (Dense wiry coat, regular hand-stripping or clipping)',
        'diet_guide': 'High-protein large-breed formula for muscular endurance and coat health.',
        'ideal_caretaker': 'Experienced owners who provide firm positive leadership and active agility.',
        'care_tips': 'Strong guarding instinct; requires early socialization and obedience training.'
    },
    'Standard Schnauzer': {
        'species': 'Dog',
        'group': 'Working / Terrier Group',
        'origin': 'Germany',
        'lifespan': '13 - 16 years',
        'weight_range': '14 - 23 kg',
        'temperament': ['Clever', 'Fearless', 'Affectionate', 'Spirited', 'Vigilant'],
        'exercise_needs': 'Moderate to High (45-60 mins daily walks, games, and agility)',
        'grooming_needs': 'Moderate to High (Signature beard and eyebrows, regular brushing)',
        'diet_guide': 'Balanced medium-breed formula with joint and skin support.',
        'ideal_caretaker': 'Active families who appreciate an intelligent, spirited watchdog.',
        'care_tips': 'Wipe beard after meals to prevent food staining and matting.'
    },
    'Husky': {
        'species': 'Dog',
        'group': 'Working / Spitz Group',
        'origin': 'Siberia, Russia',
        'lifespan': '12 - 15 years',
        'weight_range': '16 - 27 kg',
        'temperament': ['Outgoing', 'Gentle', 'Mischievous', 'Loyal', 'High Energy'],
        'exercise_needs': 'Very High (60-90 mins daily running, hiking, pulling sports)',
        'grooming_needs': 'Moderate (Dense double coat, weekly brushing, heavy seasonal blowouts)',
        'diet_guide': 'High-protein working dog diet rich in healthy fats and omega oils.',
        'ideal_caretaker': 'Athletic owners with secure fenced yards who love outdoor running.',
        'care_tips': 'Famous escape artists; ensure high fencing and never walk off-leash.'
    },
    'Cardigan Welsh Corgi': {
        'species': 'Dog',
        'group': 'Herding Group',
        'origin': 'Wales, Great Britain',
        'lifespan': '12 - 15 years',
        'weight_range': '11 - 17 kg',
        'temperament': ['Affectionate', 'Loyal', 'Alert', 'Intelligent', 'Adaptable'],
        'exercise_needs': 'Moderate (45 mins daily walking and herding ball games)',
        'grooming_needs': 'Moderate (Double coat, weekly brushing)',
        'diet_guide': 'Controlled caloric diet with joint support to maintain healthy spine weight.',
        'ideal_caretaker': 'Active families who want a loyal, sturdy, low-rider companion.',
        'care_tips': 'Distinct from Pembroke by having a long fox-like tail and larger rounded ears.'
    }
}

for k, v in dog_profiles.items():
    meta[k] = v

with open(METADATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2)

print(f"Enriched breed metadata! Total verified breed records: {len(meta)}")

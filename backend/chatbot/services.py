"""
Pet Care AI Chatbot Service Layer
Integrates local LLM with high-precision veterinary domain intelligence,
database pet profile recognition, and species-accurate nutritional engines.
"""

import requests
import json
import re
import os
from django.conf import settings
from .models import ChatHistory

SYSTEM_PROMPT = """You are "PawPal AI", an expert, warm, and highly knowledgeable Pet Care Companion Assistant.
Your mission is to provide direct, accurate, and actionable guidance for pet owners regarding:
- Pet Nutrition & Feeding Schedules (distinct for cats vs dogs, puppies, kittens, adults, seniors, exact portions, weaning, 12-month transition)
- Breed Traits & Health Vulnerabilities
- Grooming & Hygiene Routines
- Behavioral Training & Socialization (potty training, biting, crate training, leash manners)
- Vaccination Timelines & Preventive Wellness (DHPP, Rabies, FVRCP, Deworming, Flea/Tick prevention)
- Symptom Guidance & First-Aid

Response Guidelines:
- Directly and accurately answer the user's specific question. Never give dog advice to a cat owner or vice versa.
- If a pet's name is mentioned (e.g. Luna, Max, Rocky, Bella), personalize the answer for their exact species and breed.
- Use clean Markdown with bolding (**key terms**), bullet points (- ), and numbered steps (1. 2. 3.).
- For acute symptoms (persistent vomiting, bloat, toxic ingestion, breathing difficulty), always advise seeing a licensed veterinarian immediately.
"""

def extract_pet_name(query_text):
    """Detects pet name from phrases like 'how to feed my luna', 'my dog Max', 'for Bella', etc."""
    ignore_words = {
        'puppy', 'dog', 'dogs', 'cat', 'cats', 'kitten', 'kittens', 'pet', 'pets',
        'friend', 'boy', 'girl', 'baby', 'food', 'diet', 'meal', 'schedule', 'vet',
        'she', 'he', 'her', 'him', 'it', 'them', 'this', 'that', 'my', 'our', 'a', 'an', 'the'
    }

    # 1. 'my puppy Luna'
    m1 = re.search(r'\b(?:my|our)\s+(?:puppy|dog|cat|kitten|pet)\s+([A-Za-z]+)\b', query_text, re.IGNORECASE)
    if m1 and m1.group(1).lower() not in ignore_words:
        return m1.group(1).capitalize()

    # 2. 'my Luna'
    m2 = re.search(r'\b(?:my|our)\s+([A-Za-z]+)\b', query_text, re.IGNORECASE)
    if m2 and m2.group(1).lower() not in ignore_words:
        return m2.group(1).capitalize()

    # 3. 'for Luna' / 'feed Luna'
    m3 = re.search(r'\b(?:for|feed|help)\s+([A-Za-z]+)\b', query_text, re.IGNORECASE)
    if m3 and m3.group(1).lower() not in ignore_words:
        return m3.group(1).capitalize()

    return None


def find_pet_profile(name, user=None):
    """Retrieves registered pet profile from the database by name and owner."""
    if not name:
        return None
    try:
        from pets.models import Pet
        if user and user.is_authenticated:
            pet = Pet.objects.filter(owner=user, name__iexact=name).first()
            if pet:
                return pet
        # Fallback to any registered pet with this name
        return Pet.objects.filter(name__iexact=name).first()
    except Exception:
        return None


def detect_pet_age_in_months(query_text):
    """Extracts age in months from queries like '12 monts', '1 year', '6 months', '8 weeks'."""
    m = re.search(r'(\d+)\s*(months?|monts?|mos?|years?|yrs?|weeks?|wks?)\b', query_text, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        unit = m.group(2).lower()
        if unit.startswith('y'):
            return num * 12
        elif unit.startswith('w'):
            return max(1, num // 4)
        else:
            return num
    return None


def detect_navigation_intent(query_text, user=None):
    """
    Detects if user asks to navigate to a specific page or feature across Pet Care Companion.
    Returns direct action URL, human title, and formatted markdown jump links.
    """
    if not query_text:
        return None

    raw_q = query_text.strip().lower()
    q = re.sub(r'[^\w\s]', ' ', raw_q)
    q = re.sub(r'\s+', ' ', q).strip()

    has_nav_verb = any(v in raw_q for v in [
        'go to', 'goto', 'open', 'take me to', 'navigate to', 'show me', 'bring me to',
        'redirect to', 'move to', 'head to', 'visit', 'where is', 'link to', 'jump to',
        'switch to', 'show', 'view', 'access', 'po', 'poga', 'poganum'
    ])

    # 1. DASHBOARD
    if any(k in q for k in ['dashboard', 'dash board', 'home dash', 'main dash']) or (has_nav_verb and ('dashboard' in q or 'dash board' in q or 'dash' in q)):
        dash_url = '/users/dashboard/'
        if user and getattr(user, 'role', '').upper() == 'CARETAKER':
            dash_url = '/users/dashboard/caretaker/'
        elif user and getattr(user, 'role', '').upper() == 'PET_OWNER':
            dash_url = '/users/dashboard/owner/'
        return {
            'destination': 'Dashboard',
            'redirect_url': dash_url,
            'response': "🚀 **Redirecting to Dashboard...**"
        }

    # 2. ADD PET / CREATE PET
    if any(k in q for k in ['add pet', 'create pet', 'register pet', 'new pet', 'add a pet', 'register a pet', 'add new pet']):
        return {
            'destination': 'Add Pet',
            'redirect_url': '/pets/add/',
            'response': "🚀 **Redirecting to Add New Pet...**"
        }

    # 3. MY PETS / PET LIST / PET PROFILES
    if any(k in q for k in ['my pets', 'pets list', 'pet list', 'my pet list', 'pet profiles', 'view pets', 'all pets']) or (has_nav_verb and ('pet' in q or 'pets' in q) and not any(w in q for w in ['food', 'feed', 'diet', 'sick', 'vaccine', 'groom', 'train', 'bark', 'bite'])):
        return {
            'destination': 'My Pets',
            'redirect_url': '/pets/',
            'response': "🚀 **Redirecting to My Pets...**"
        }

    # 4. REPORT LOST PET
    if any(k in q for k in ['report lost', 'report a lost', 'report missing', 'report found', 'i lost my pet', 'my pet is lost', 'file lost pet']):
        return {
            'destination': 'Report Lost Pet',
            'redirect_url': '/lostfound/report/',
            'response': "🚀 **Redirecting to Report Lost Pet...**"
        }

    # 5. LOST AND FOUND NETWORK
    if any(k in q for k in ['lost and found', 'lost & found', 'lost found', 'missing pets', 'found pets', 'lost pet list']) or (has_nav_verb and 'lost' in q):
        return {
            'destination': 'Lost & Found Network',
            'redirect_url': '/lostfound/',
            'response': "🚀 **Redirecting to Lost & Found Network...**"
        }

    # 6. HEALTH TRACKER / VACCINE REMINDERS / WEIGHT
    if any(k in q for k in ['health tracker', 'health reminders', 'vaccine reminders', 'vaccination reminders', 'weight tracker', 'weight log', 'medical tracker']) or (has_nav_verb and 'health' in q):
        return {
            'destination': 'Health Tracker',
            'redirect_url': '/health/reminders/',
            'response': "🚀 **Redirecting to Health Tracker...**"
        }

    # 7. SMART RECOMMENDATIONS / MATCHING CARETAKERS
    if any(k in q for k in ['recommendation', 'recommendations', 'smart recommend', 'smart recommendation', 'match caretaker', 'match caretakers', 'recommend caretaker', 'caretaker match']) or (has_nav_verb and 'recommend' in q):
        return {
            'destination': 'Smart Recommendations',
            'redirect_url': '/recommendations/',
            'response': "🚀 **Redirecting to Smart Recommendations...**"
        }

    # 8. AI BREED SCANNER / BREED DETECTION
    if any(k in q for k in ['breed scanner', 'breed detector', 'detect breed', 'identify breed', 'breed detection', 'scan breed', 'ai breed', 'photo breed']) or (has_nav_verb and 'breed' in q and ('scan' in q or 'detect' in q or 'identify' in q or 'camera' in q or 'upload' in q)):
        return {
            'destination': 'AI Breed Scanner',
            'redirect_url': '/breed-detection/',
            'response': "🚀 **Redirecting to AI Breed Scanner...**"
        }

    # 9. CARETAKER MARKETPLACE
    if any(k in q for k in ['marketplace', 'caretaker marketplace', 'find caretaker', 'find sitters', 'pet sitters', 'caretakers list']) or (has_nav_verb and ('marketplace' in q or 'caretaker' in q or 'sitter' in q)):
        return {
            'destination': 'Caretaker Marketplace',
            'redirect_url': '/marketplace/',
            'response': "🚀 **Redirecting to Caretaker Marketplace...**"
        }

    # 10. BOOKINGS / APPOINTMENTS
    if any(k in q for k in ['booking', 'bookings', 'my bookings', 'my appointments', 'booking list', 'view bookings', 'booking requests']) or (has_nav_verb and ('booking' in q or 'appointment' in q)):
        booking_url = '/bookings/caretaker/requests/' if (user and getattr(user, 'role', '') == 'caretaker') else '/bookings/my-bookings/'
        return {
            'destination': 'My Bookings',
            'redirect_url': booking_url,
            'response': "🚀 **Redirecting to Bookings & Appointments...**"
        }

    # 11. PROFILE / ACCOUNT SETTINGS
    if any(k in q for k in ['profile', 'my profile', 'user profile', 'account settings', 'edit profile', 'my account', 'profile page', 'account']) or (has_nav_verb and ('profile' in q or 'account' in q)):
        return {
            'destination': 'My Profile',
            'redirect_url': '/users/profile/',
            'response': "🚀 **Redirecting to My Profile...**"
        }

    # 12. ADOPTION HUB
    if any(k in q for k in ['adoption hub', 'adopt pet', 'adopt a pet', 'pet adoption', 'adoption listings']) or (has_nav_verb and 'adopt' in q):
        return {
            'destination': 'Adoption Hub',
            'redirect_url': '/adoption/',
            'response': "🚀 **Redirecting to Pet Adoption Hub...**"
        }

    # 13. MATCHHUB
    if any(k in q for k in ['matchhub', 'match hub', 'pet dating', 'pet playmates', 'pet mate']) or (has_nav_verb and 'match' in q and not 'caretaker' in q):
        return {
            'destination': 'MatchHub',
            'redirect_url': '/matchhub/',
            'response': "🚀 **Redirecting to MatchHub...**"
        }

    # 14. HOME
    if q in ['home', 'homepage', 'home page', 'main page'] or (has_nav_verb and 'home' in q):
        return {
            'destination': 'Home',
            'redirect_url': '/',
            'response': "🚀 **Redirecting to Homepage...**"
        }

    return None


def query_domain_knowledge_base(query_text, user=None):
    """
    High-precision veterinary domain knowledge engine providing tailored, accurate answers.
    Personalizes based on registered pet profiles in the database.
    """
    # 0. Check for Navigation intent
    nav_intent = detect_navigation_intent(query_text, user=user)
    if nav_intent:
        return nav_intent['response']

    q = query_text.lower().strip()
    pet_name = extract_pet_name(query_text)
    pet_profile = find_pet_profile(pet_name, user=user)
    age_months = detect_pet_age_in_months(query_text)

    # Detect explicit or inferred species
    is_explicit_cat = any(w in q for w in ['cat', 'cats', 'kitten', 'kittens', 'kitty', 'feline'])
    is_explicit_dog = any(w in q for w in ['dog', 'dogs', 'puppy', 'puppies', 'pup', 'canine', 'hound'])

    inferred_species = None
    if is_explicit_cat:
        inferred_species = 'Cat'
    elif is_explicit_dog:
        inferred_species = 'Dog'
    elif pet_profile:
        inferred_species = pet_profile.species

    gender_pronoun = "She" if re.search(r'\b(she|her)\b', q) else ("He" if re.search(r'\b(he|him|his)\b', q) else "Your pet")

    is_food_query = any(w in q for w in ['food', 'feed', 'diet', 'eat', 'meal', 'nutrition', 'portion', 'kibble', 'hungry', 'eating', 'remommend', 'recommend', 'schedule', 'calorie', 'toppers', 'how to feed'])

    # =========================================================================
    # 1. PERSONALIZED PET PROFILE FEEDING (e.g. Luna, Max, Bella, Rocky)
    # =========================================================================
    if is_food_query and pet_profile:
        p_name = pet_profile.name
        p_species = pet_profile.species
        p_breed = pet_profile.breed
        p_age = pet_profile.age
        p_weight = float(pet_profile.weight) if pet_profile.weight else None

        if p_species == 'Cat':
            cal_req = int(p_weight * 50) if p_weight else 220
            return f"""🐱 **Tailored Feline Nutrition & Feeding Guide for {p_name} ({p_breed}, {p_age} Years Old):**

As an adult {p_breed}, **{p_name}** is an **obligate carnivore** requiring specialized high-protein nutrition, essential **Taurine**, and high-moisture hydration to maintain healthy kidneys and urinary tract function.

---

### 🍽️ Daily Portion & Schedule for {p_name}{f' ({p_weight} kg)' if p_weight else ''}:
- **Daily Caloric Goal:** ~**{cal_req} to {cal_req + 30} kcal/day**.
- **Meal Frequency:** **2 portioned meals daily** (Morning & Evening, spaced ~10–12 hours apart).
- **Optimal Balanced Daily Routine:**
  - **Morning Bowl:** 1 can / pouch of high-protein wet canned cat food (rich in moisture and animal protein).
  - **Evening Bowl:** Approx. **30–40g** of measured indoor adult dry kibble (with hairball control and omega fatty acids for her plush coat).

---

### 🥩 Key Nutritional Requirements for {p_name}:
1. **Animal-Derived Protein First:** Real chicken, salmon, turkey, or ocean fish should be the #1 ingredient (**30%–40% Crude Protein**).
2. **Essential Taurine & Arachidonic Acid:** Crucial for feline heart muscle function and retinal vision.
3. **Hairball & Coat Health:** Natural prebiotic fiber (pumpkin, beet pulp) and Omega-3 & 6 oils to prevent hairball vomiting.
4. **Fresh Water Hydration:** Cats have low natural thirst; provide a circulating water fountain away from the food bowl.

---

### ⚠️ Strictly Forbidden for Cats:
- **Never feed dog food** (lacks sufficient taurine and vitamin A; causes heart failure and blindness).
- **Never feed cow's milk** (most adult cats are lactose intolerant; causes severe diarrhea).
- **Deadly toxins:** Lilies (fatal kidney toxicity), onions, garlic, chocolate, grapes, and xylitol."""

        else: # Dog
            cal_req = int(p_weight * 30) if p_weight else 800
            return f"""🐕 **Tailored Canine Nutrition & Feeding Guide for {p_name} ({p_breed}, {p_age} Years Old):**

As an active {p_breed}, **{p_name}** requires a nutrient-dense, balanced diet supporting lean muscle mass, joint mobility, and sustained daily energy.

---

### 🍽️ Daily Portion & Schedule for {p_name}{f' ({p_weight} kg)' if p_weight else ''}:
- **Daily Caloric Goal:** ~**{cal_req} to {cal_req + 100} kcal/day**.
- **Meal Frequency:** **2 measured meals daily** (Morning & Evening, spaced ~10–12 hours apart).
- **Daily Portion Guideline:** Divide {p_name}'s daily food into **2 equal bowls**. Always measure using a standard measuring cup rather than estimating by hand.

---

### 🥩 Key Nutritional Requirements for {p_name}:
1. **Named Animal Protein First:** Real deboned chicken, lamb, beef, or salmon (**22%–28% Crude Protein**).
2. **Healthy Fats & Joint Care:** Chicken fat, fish oil, and Glucosamine/Chondroitin for cartilage and hip support.
3. **Digestible Fiber:** Brown rice, oats, sweet potatoes, or pumpkin for smooth digestive transit.

---

### 🥗 Healthy Fresh Toppers for {p_name}:
- **Plain Boiled Boneless Chicken Breast** (unseasoned)
- **1–2 Tablespoons Plain Pumpkin Puree** (promotes firm stools)
- **Steamed Carrots or Green Beans** (low-calorie fiber crunch)
- **1 Cooked Egg** (1–2 times weekly for a shiny coat)

---

### ⚠️ Safety & Bloat Prevention:
- **Rest After Meals:** Avoid vigorous running or agility for at least 45 minutes after eating to prevent dangerous gastric bloat (GDV).
- **Strictly Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol sweetener, and cooked bones."""

    # =========================================================================
    # 2. CAT / KITTEN FEEDING (When query mentions Cat, Kitten, Kitty)
    # =========================================================================
    if is_food_query and (inferred_species == 'Cat' or is_explicit_cat or 'cat' in q or 'kitten' in q or 'kitty' in q):
        kitten_str = "Kitten" if ('kitten' in q or 'kitty' in q or (age_months and age_months < 12)) else "Cat"
        return f"""🐱 **Feline Nutrition & Feeding Guide for your {kitten_str}:**

Cats are **obligate carnivores**, which means their bodies strictly require animal-derived protein, essential **Taurine**, and dietary moisture.

---

### 📅 Feeding Schedule & Meal Frequency:
- **Kittens (2 to 6 Months):** Feed **3 to 4 portioned meals daily** of high-protein kitten wet/dry formula. Wet food is essential for early urinary hydration.
- **Junior Cats (6 to 12 Months):** Feed **2 to 3 meals daily**.
- **Adult Cats (1+ Years):** Feed **2 portioned meals daily** (approx. **200–250 kcal/day** depending on body weight).

---

### 🥩 What Makes High-Quality Feline Food:
1. **High Animal Protein:** Look for real meat/poultry as the first ingredient (**30%–40%+ protein**).
2. **Essential Amino Acids:** Guaranteed **Taurine** and **Arachidonic acid** to prevent retinal degeneration and dilated cardiomyopathy.
3. **Moisture Rich:** Incorporate wet canned food daily to prevent urinary crystals (FLUTD) and chronic kidney disease.

---

### ⚠️ Essential Feline Rules:
- **Never feed dog food to cats** (dog food lacks adequate taurine, causing fatal heart and eye deficiencies).
- **Never give cow's milk** (most cats are lactose intolerant; causes severe stomach cramps and diarrhea).
- **Toxic to Cats:** Lilies (even lily pollen is fatal), onions, garlic, chocolate, grapes, and paracetamol/ibuprofen."""

    # =========================================================================
    # 3. 12-MONTH TRANSITION (When query mentions 12 months / 1 year)
    # =========================================================================
    if is_food_query and (age_months == 12 or '12 month' in q or '12 mont' in q or '1 year' in q or '1 yr' in q):
        return f"""🥣 **Tailored 12-Month (1 Year) Nutrition & Feeding Guide:**

At **12 months of age**, {gender_pronoun.lower()} is reaching physical adulthood! This is the milestone to transition from calorie-dense puppy/kitten food to a **complete Adult Maintenance Diet**.

---

### 🔄 1. The 7-Day Safe Transition Schedule
*Never switch foods overnight, as sudden changes trigger acute diarrhea and vomiting.*
- **Days 1 & 2:** 75% Current Junior Food + **25% New Adult Food**
- **Days 3 & 4:** 50% Current Food + **50% New Adult Food**
- **Days 5 & 6:** 25% Current Food + **75% New Adult Food**
- **Day 7 Onward:** **100% High-Quality Adult Formula**

---

### 🍽️ 2. Daily Portion & Meal Frequency
- **Frequency:** **2 meals per day** (Morning & Evening, separated by ~10–12 hours).
- **Daily Portion:** Measure approximately **2.5% to 3.0% of ideal body weight** in total daily food, divided into morning and evening bowls.

---

### 🥗 3. Healthy Fresh Toppers:
- Plain Boiled Boneless Chicken Breast
- 1–2 Tablespoons Plain Pumpkin Puree (promotes firm digestion)
- Steamed Carrots or Green Beans
- 1 Cooked Egg (1–2 times weekly)

---

### ⚠️ 4. Strictly Avoid:
- Onions, garlic, chocolate, grapes, raisins, xylitol sweetener, cooked bones."""

    # =========================================================================
    # 4. GENERAL DOG / PUPPY FEEDING
    # =========================================================================
    if is_food_query and (inferred_species == 'Dog' or is_explicit_dog or 'dog' in q or 'puppy' in q or 'pup' in q):
        puppy_str = "Puppy" if ('puppy' in q or 'pup' in q or (age_months and age_months < 12)) else "Dog"
        name_str = f"for **{pet_name}**" if pet_name else "for your dog"
        return f"""🐕 **Canine Nutrition & Feeding Guide {name_str}:**

Dogs are omnivorous carnivores that thrive on high-grade animal protein, healthy fats, and easily digestible fiber.

---

### 📅 Feeding Schedule & Meal Frequency:
- **Puppies (6 to 12 Weeks):** **4 meals daily** (Soften puppy kibble with warm water/broth).
- **Puppies (3 to 6 Months):** **3 meals daily** (Crunchy dry kibble to soothe teething).
- **Puppies (6 to 12 Months):** **2 meals daily** (Morning & evening portions).
- **Adult Dogs (1+ Years):** **2 meals daily** (Morning & evening, separated by 10–12 hours).

---

### 🍽️ Daily Portion & Calorie Formula:
- An active adult dog requires roughly **30 calories per kg of ideal body weight daily**.
- Check the feeding guidelines chart on your kibble bag based on target adult weight and divide into 2 equal bowls.
- **Body Condition:** You should easily feel the ribs under a light layer of skin with a visible waistline from above.

---

### ⚠️ Safety & Bloat (GDV) Prevention:
- Avoid vigorous running or jumping for at least 45 minutes after meals.
- **Strictly Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol sweetener, cooked bones, macadamia nuts."""

    # =========================================================================
    # 5. GENERAL PET FEEDING (If name specified like Luna, Max without species in query)
    # =========================================================================
    if is_food_query:
        name_str = f"for **{pet_name}**" if pet_name else "for your pet"
        return f"""🥣 **Tailored Nutrition & Feeding Guide {name_str}:**

### 🐶 If {name_str.replace('for ', '')} is a Dog:
- **Meal Frequency:** **2 meals per day** (Morning & Evening).
- **Portion Guideline:** ~**30 calories per kg of ideal body weight** daily.
- **Diet Balance:** Real animal meat first (**22%–28% Protein**), healthy fats, joint-supporting glucosamine, and fiber.
- **Safe Toppers:** Boiled chicken, pumpkin puree, steamed carrots, cooked eggs.
- **Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol, cooked bones.

---

### 🐱 If {name_str.replace('for ', '')} is a Cat:
- **Meal Frequency:** **2 to 3 portioned meals per day**.
- **Obligate Carnivore:** High animal protein (**30%–40%+**) and essential **Taurine** (prevents blindness and heart disease).
- **Hydration:** Feed high-moisture canned wet food daily to protect kidney and urinary tract health.
- **Toxic:** Dog food (lacks taurine), cow's milk (lactose intolerance), lilies, onions, garlic."""

    # =========================================================================
    # 6. STRICTLY TOXIC FOODS
    # =========================================================================
    if any(w in q for w in ['toxic', 'poison', 'harmful', 'chocolate', 'grape', 'onion', 'garlic', 'raisin', 'xylitol', 'can my dog eat', 'can my cat eat', 'safe food']):
        return """⚠️ **Strictly Toxic & Dangerous Foods for Pets:**

1. **Chocolate, Coffee & Caffeine:** Contains *Theobromine* which triggers rapid heartbeat, tremors, seizures, and heart failure.
2. **Grapes & Raisins:** Even a tiny quantity can cause acute, irreversible kidney failure in dogs.
3. **Onions, Garlic, Leeks & Chives:** Contains *N-propyl disulfide* which destroys red blood cells, causing severe hemolytic anemia in cats and dogs.
4. **Xylitol / Birch Sugar:** Found in sugar-free peanut butter, candies, and baked goods. Triggers a massive insulin surge leading to acute liver failure.
5. **Cooked Bones:** Splinter easily into sharp shards that puncture the stomach or intestines.
6. **Lilies (For Cats):** Ingestion of even a leaf, petal, or pollen causes fatal acute kidney failure in cats.
7. **Macadamia Nuts & Walnuts:** Cause temporary paralysis, vomiting, hyperthermia, and muscle tremors.

*🚨 If you suspect toxic ingestion, contact your nearest emergency veterinarian immediately.*"""

    # =========================================================================
    # 7. VACCINATION TIMELINES & PREVENTIVE SHOTS
    # =========================================================================
    if any(w in q for w in ['vaccin', 'shot', 'rabies', 'dhpp', 'fvrcp', 'deworm', 'immuniz']):
        return """💉 **Complete Pet Vaccination & Preventive Health Schedule:**

### 🐶 Canine Core Vaccination Timetable:
- **6 to 8 Weeks:** **DHPP Dose 1** (Distemper, Infectious Hepatitis, Parvovirus, Parainfluenza) + Initial Deworming.
- **10 to 12 Weeks:** **DHPP Dose 2** + **Bordetella** (Kennel Cough) + Leptospirosis.
- **14 to 16 Weeks:** **DHPP Dose 3 (Final Booster)** + **Rabies 1-Year Vaccine**.
- **Adult Boosters:** Rabies booster every 1 to 3 years; DHPP booster annually or triennially.
- **Deworming:** Routine broad-spectrum deworming every 3 months.

### 🐱 Feline Core Vaccination Timetable:
- **8 Weeks:** **FVRCP Dose 1** (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia).
- **12 Weeks:** **FVRCP Dose 2** + FeLV (Feline Leukemia for outdoor/multicat).
- **16 Weeks:** **FVRCP Final Booster** + **Rabies Vaccine**.
- **Adult Boosters:** FVRCP every 1-3 years; Rabies annually."""

    # =========================================================================
    # 8. POTTY & BEHAVIORAL TRAINING
    # =========================================================================
    if any(w in q for w in ['potty', 'toilet', 'pee', 'poop', 'housebreak', 'crate', 'train', 'biting', 'barking', 'chew']):
        if any(w in q for w in ['bite', 'chew', 'nipping', 'teeth']):
            return """🦷 **Puppy Biting & Chewing Solution:**
- **Why Puppies Bite:** Puppies explore with their mouths and suffer from itchy gums during teething (3 to 6 months).
- **The High-Pitched Yelp:** When teeth touch human skin, immediately emit a high-pitched *"Ouch!"*, freeze your hand, and turn away for 15 seconds.
- **Instant Redirection:** Always keep a durable rubber chew toy handy. Swap your hand with the toy and praise enthusiastically when they chew the toy.
- **Never Use Physical Punishment:** Striking or grabbing the muzzle increases fear and defensive aggression."""

        return """🐾 **Step-by-Step Puppy Potty Training Protocol:**

1. **The 2-Hour Golden Rule:** Take your puppy to the designated outdoor elimination spot:
   - Immediately upon waking in the morning and after naps.
   - 10 to 20 minutes after every meal or water bowl visit.
   - Immediately following energetic play sessions.
   - At least once every 2 hours during the day.
2. **Pick a Designated Spot & Cue Word:** Take them to the exact same patch of grass and repeat a calm cue like *"Go Potty"*.
3. **The 3-Second Reward Window:** The very second they finish eliminating outside, shower them with high-value treats and enthusiastic praise.
4. **Never Punish Accidents:** Clean indoor accidents thoroughly with an enzymatic cleaner to erase urine pheromone traces."""

    # =========================================================================
    # 9. GROOMING & BATHING
    # =========================================================================
    if any(w in q for w in ['groom', 'bath', 'brush', 'nail', 'teeth', 'shedding', 'coat', 'wash']):
        return """🛁 **Pet Grooming & Hygiene Master Guide:**

- **Bathing Frequency:** Dogs should be bathed once every **3 to 5 weeks** using a pH-balanced, oatmeal-based dog shampoo. Over-bathing strips essential protective sebum and causes dry, itchy dermatitis.
- **Coat Brushing:** 
  - *Short Coats (Labradors, Beagles):* Rubber curry brush or bristle brush once weekly.
  - *Double Coats (Golden Retrievers, Huskies, German Shepherds):* Undercoat rake 3-4 times weekly. **Never shave double coats** as it ruins their thermal regulation.
  - *Long/Silky Coats (Persians, Shih Tzus):* Daily wide-tooth comb to prevent painful pelt matting.
- **Nail Trimming:** Clip every 3 to 4 weeks. Always avoid the pink interior blood vessel (the *quick*).
- **Dental Hygiene:** Brush teeth 2–3 times per week with veterinary enzymatic toothpaste (never human toothpaste containing toxic fluoride)."""

    # =========================================================================
    # 10. POPULAR BREEDS
    # =========================================================================
    if any(w in q for w in ['labrador', 'golden retriever', 'german shepherd', 'husky', 'beagle', 'persian', 'siamese', 'french bulldog', 'shih tzu', 'poodle', 'maine coon', 'abyssinian', 'affenpinscher']):
        if 'abyssinian' in q:
            return "🐱 **Abyssinian Cat Guide:** Highly intelligent, playful, and agile. They love high climbing trees and puzzle toys. Feed high-protein feline nutrition rich in taurine for their lean, athletic build."
        elif 'affenpinscher' in q:
            return "🐶 **Affenpinscher Guide:** 'The Monkey Dog' – spirited, loyal, and comical toy terrier. Keep up weekly coat brushing to prevent beard matting, and maintain moderate daily walking."
        elif 'beagle' in q:
            return "🐶 **Beagle Guide:** Driven by scent hound instincts. Always keep on-leash in open areas. Keep human garbage locked up as they have voracious appetites and are prone to obesity."
        elif 'labrador' in q:
            return "🐶 **Labrador Retriever Guide:** Labs are intelligent, energetic, and eager to please. They require **60–90 minutes of daily physical exercise** (retrieving, swimming, trail walking). Prone to genetic hip/elbow dysplasia and obesity; maintain strict portion control and feed joint-supporting glucosamine."
        elif 'golden' in q:
            return "🐶 **Golden Retriever Guide:** Affectionate and gentle companions. They need daily mental stimulation, brushing 3-4 times weekly to prevent matting, and keeping floppy ears dry after swimming to prevent bacterial ear infections."
        elif 'shepherd' in q:
            return "🐶 **German Shepherd Guide:** High-drive working dogs requiring structured obedience training, agility, and 90+ minutes of daily exercise. Early socialization with children and other animals channels their natural protective instincts safely."
        elif 'husky' in q:
            return "🐺 **Siberian Husky Guide:** High-endurance athletic dogs. Require vigorous exercise and escape-proof 6ft+ yard fences. Never shave their double coat in hot weather."
        elif 'french' in q or 'bulldog' in q:
            return "🐶 **French Bulldog Guide:** Brachycephalic (flat-faced) breed sensitive to heat exhaustion. Walk during cool mornings/evenings, avoid strenuous hot weather exercises, and clean facial skin folds weekly."
        elif 'persian' in q:
            return "🐱 **Persian Cat Guide:** Calm, indoor feline. Their dense, plush coat requires daily gentle combing from root to tip. Gently wipe eye corners with a damp sterile cotton pad daily to clear tear stains."
        elif 'siamese' in q:
            return "🐱 **Siamese Cat Guide:** Highly vocal, deeply social, and affectionate. They thrive on interactive puzzle games, vertical cat towers, and quality bonding time."

    # =========================================================================
    # 11. COMMON SYMPTOMS & HEALTH WARNINGS
    # =========================================================================
    if any(w in q for w in ['vomit', 'diarrhea', 'sick', 'lethargic', 'not eating', 'fever', 'cough', 'scratching', 'flea', 'tick', 'ear']):
        if any(w in q for w in ['scratch', 'itch', 'flea', 'tick']):
            return """🪲 **Itching, Fleas & Skin Care Advice:**
- **Flea & Tick Prevention:** Apply a vet-approved monthly spot-on treatment (like Fipronil or Fluralaner chewable).
- **Check for Flea Dirt:** Part the fur near the base of the tail and belly; look for tiny black pepper-like specks.
- **Soothing Skin:** Bathe in cool water with colloidal oatmeal shampoo to relieve acute allergic itching."""

        return """🩺 **Health & Symptom Guidance:**

### 🩹 Mild Symptoms (Single skipped meal / soft stool):
- If your pet is energetic, alert, and drinking water, fast them for 4–6 hours (adults only; do not fast puppies/kittens under 6 months).
- Offer a bland recovery meal of **plain boiled boneless chicken breast + boiled white rice (50/50 ratio)** in small portions.

### 🚨 Seek Immediate Emergency Veterinary Care If:
- Continuous vomiting or inability to keep water down for over 6 hours.
- Dark black tarry stool or bloody diarrhea.
- Extreme lethargy, pale white gums, or inability to stand.
- Swollen, distended, or hard abdomen with unproductive retching (sign of GDV bloat).
- Known or suspected toxic ingestion (medications, chocolate, raisins, chemicals)."""

    # =========================================================================
    # 12. DEFAULT FRIENDLY RESPONSE
    # =========================================================================
    name_prefix = f"for **{pet_name}**" if pet_name else "for your pet"
    return f"""🐾 Hello! I am your **Pet Care Companion AI Assistant**.

I am ready to help {name_prefix} with:
- **Optimal Feeding Plans & Daily Portion Schedules** (Puppies, Kittens, Adults, Seniors)
- **Safe vs. Toxic Foods List**
- **Puppy/Kitten Potty & Behavioral Training**
- **Complete Vaccination & Preventive Deworming Schedules**
- **Coat Grooming & Hygiene Best Practices**
- **Breed Identification & Exercise Guidance**

*Ask me any specific question about your furry friend to get started!*"""


def get_ai_chat_response(query_text, user=None, session_id='guest'):
    """
    Returns high-accuracy response from navigation router, local LLM (Ollama), or veterinary intelligence fallback.
    """
    if not query_text or not query_text.strip():
        return {
            'response': "Please enter a question so I can assist you with your pet care needs!",
            'model': 'PawPal AI'
        }

    # 0. Check for Navigation & Platform Action Intent FIRST
    nav_intent = detect_navigation_intent(query_text, user=user)
    if nav_intent:
        try:
            ChatHistory.objects.create(
                user=user if (user and user.is_authenticated) else None,
                session_id=session_id,
                user_query=query_text,
                bot_response=nav_intent['response'],
                model_used='PawPal Navigator'
            )
            from config.mongodb import log_chat_to_mongodb
            log_chat_to_mongodb(
                user_id=user.id if (user and user.is_authenticated) else None,
                username=user.username if (user and user.is_authenticated) else 'Guest',
                query=query_text,
                response=nav_intent['response'],
                source='PawPal Navigator'
            )
        except Exception:
            pass
        return {
            'response': nav_intent['response'],
            'model': 'PawPal Navigator',
            'redirect_url': nav_intent.get('redirect_url'),
            'destination': nav_intent.get('destination'),
            'action': 'navigate'
        }

    # 1. Attempt Local Ollama LLM Inference if configured
    ollama_url = getattr(settings, 'OLLAMA_API_URL', 'http://localhost:11434/api/generate')
    ollama_model = getattr(settings, 'OLLAMA_MODEL_NAME', 'qwen:4b')

    try:
        payload = {
            "model": ollama_model,
            "prompt": f"{SYSTEM_PROMPT}\n\nUser Question: {query_text}\n\nAssistant Response:",
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
            }
        }
        res = requests.post(ollama_url, json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            llm_text = data.get('response', '').strip()
            if llm_text and len(llm_text) > 40:
                try:
                    ChatHistory.objects.create(
                        user=user if (user and user.is_authenticated) else None,
                        session_id=session_id,
                        user_query=query_text,
                        bot_response=llm_text,
                        model_used=f"Ollama ({ollama_model})"
                    )
                    from config.mongodb import log_chat_to_mongodb
                    log_chat_to_mongodb(
                        user_id=user.id if (user and user.is_authenticated) else None,
                        username=user.username if (user and user.is_authenticated) else 'Guest',
                        query=query_text,
                        response=llm_text,
                        source=f"Ollama ({ollama_model})"
                    )
                except Exception:
                    pass
                return {
                    'response': llm_text,
                    'model': f"Ollama ({ollama_model})"
                }
    except Exception:
        pass

    # 2. High-precision Veterinary Knowledge Base (with User Profile context)
    domain_response = query_domain_knowledge_base(query_text, user=user)

    try:
        ChatHistory.objects.create(
            user=user if (user and user.is_authenticated) else None,
            session_id=session_id,
            user_query=query_text,
            bot_response=domain_response,
            model_used='PawPal Veterinary Intelligence'
        )
        from config.mongodb import log_chat_to_mongodb
        log_chat_to_mongodb(
            user_id=user.id if (user and user.is_authenticated) else None,
            username=user.username if (user and user.is_authenticated) else 'Guest',
            query=query_text,
            response=domain_response,
            source='PawPal Veterinary Intelligence'
        )
    except Exception:
        pass

    return {
        'response': domain_response,
        'model': 'PawPal Veterinary Intelligence'
    }

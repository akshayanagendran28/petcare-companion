# Pet Care Companion – AI-Powered Pet Care and Marketplace Platform

**Pet Care Companion** is a modern, full-stack, AI/ML-driven web application designed to connect pet owners with certified caretakers, manage pet health with automatic vaccination reminders, facilitate pet adoption and companion matching, generate digital QR Pet ID cards, and provide 24/7 intelligent pet care guidance using local LLMs and trained Machine Learning models.

---

## 🐾 Key Features

- **Caretaker Marketplace & Booking Workflow**: Multi-criteria search (price, rating, experience, service, availability), auto-calculated pricing, booking state machine (`PENDING` → `ACCEPTED` / `REJECTED` → `COMPLETED` → `REVIEWED`).
- **Dynamic QR Pet ID Card**: Automatically generates high-resolution QR codes linking to public emergency profiles (`/pets/<id>/emergency/`) for instant owner contact and critical medical info. Printable/downloadable ID badge layout included.
- **ML Feature 1 — Smart Recommendation System**: Genuine Scikit-Learn Multi-Output Random Forest model trained on pet age, weight, breed, health conditions, and activity levels. Delivers tailored diet formulas, compatible caretaker rankings with match scores, and daily care tips.
- **ML Feature 2 — Pet Breed Identification**: Computer vision classifier extracting multi-channel visual moments and luminance descriptors across 15 dog and cat breeds with top-3 rankings, confidence percentages, and 1-click interlocks to the recommendation and chatbot engines.
- **Local AI Chatbot (Ollama + Qwen3 4B)**: Embedded as a global floating widget on **every single page** (`base.html`) and as a dedicated assistant page. Stores full chat history in the database with domain rule fallback.
- **Health Tracker & Preventive Reminders**: Chart.js interactive weight tracking, vaccination logs with urgency badges (`Upcoming`, `Due Soon`, `Overdue`), active prescriptions, and allergy records.
- **Pet Adoption & Marketplace**: Publish adoption/sale listings with species, location, price, and direct guardian contact channels.
- **Pet Match Hub**: Companion matching for playdates, walking buddies, and pedigree breeding with incoming/outgoing requests.
- **Community Lost & Found Board**: Urgent missing pet alerts with sighting submission and direct owner notification.
- **Three.js 3D Background**: Subtle interactive 3D particle background with floating glowing elements and mouse parallax.
- **Oracle Database Readiness**: 17 normalized tables with constraints, indexes, sequences, and DDL schema script (`oracle_sql/schema_ddl.sql`).

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Three.js, Chart.js, Font Awesome 6, Glassmorphism |
| **Backend** | Python 3.12, Django 4.2, Django ORM, Django Forms, Django REST Framework |
| **Database** | **Oracle Database** (Oracle XE / Free / 19c / 21c / 23ai) via `python-oracledb` (with instant local dev switch) |
| **AI Chatbot** | **Ollama** running **Qwen3 4B** (`http://localhost:11434/api/generate`) |
| **Machine Learning** | **Scikit-Learn**, **NumPy**, **Pandas**, **Pillow**, **Joblib** |
| **QR Engine** | `qrcode` Python library with PIL image rendering |

---

## 📁 Project Structure

The project is organized into three clean, dedicated tiers: **Frontend**, **Backend**, and **Database**:

```
pet_care_companion/
│
├── frontend/                  # Presentation Tier
│   ├── templates/             # Server-rendered HTML5 Django templates
│   │   ├── base.html          # Global layout, navbar, footer & chatbot widget
│   │   ├── home.html          # Landing page
│   │   ├── bookings/          # Multi-pet booking, availability ribbon & UPI checkout
│   │   ├── marketplace/       # Caretaker discovery & verified profiles
│   │   ├── pets/              # Pet registration, QR codes & health cards
│   │   ├── adoption/          # Pet adoption listings & applications
│   │   ├── health/            # Medical records, weight charts & reminders
│   │   ├── lostfound/         # Missing pet reports & community sightings
│   │   └── ...                # App-specific templates
│   ├── static/                # Static assets (CSS, JS, images, avatars)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── README.md              # Frontend architecture documentation
│
├── backend/                   # Business Logic & API Tier
│   ├── config/                # Django core settings, routing & WSGI/ASGI
│   ├── users/                 # RBAC authentication & dashboards
│   ├── pets/                  # Pet entity management & QR generation
│   ├── bookings/              # 1-booking/day capacity & emergency booking flow
│   ├── marketplace/           # Caretaker profiles & pricing
│   ├── adoption/              # Adoption pipeline & requests
│   ├── health/                # Vaccination tracking & health logs
│   ├── lostfound/             # Lost & found pet geo-reporting
│   ├── matchhub/              # Playdate matchmaking
│   ├── chatbot/               # Conversational AI assistant
│   ├── breed_detection/       # MobileNetV2 ONNX breed classification
│   ├── recommendations/       # Machine learning recommendation engine
│   ├── reviews/               # Verified caretaker star ratings
│   ├── notifications/         # Real-time event notifications
│   ├── ml/                    # ML training pipelines
│   ├── ml_models/             # ONNX weights & serialized models
│   ├── datasets/              # Pet datasets (Oxford-IIIT Pet & care CSVs)
│   ├── manage.py              # Backend utility runner
│   ├── requirements.txt       # Backend dependencies
│   └── README.md              # Backend architecture documentation
│
├── database/                  # Data Persistence Tier
│   ├── schema.sql             # SQL schema DDL definitions
│   ├── schema_dump.sql        # Full database dump with tables & seed rows
│   ├── oracle/                # Oracle Database DDL scripts & setup guide
│   └── README.md              # Database setup & migration documentation
│
├── media/                     # User uploads (pet photos, documents, receipts)
├── manage.py                  # Root management utility
├── requirements.txt           # Project dependencies
├── tests_system.py            # Comprehensive system test suite
└── README.md                  # Project overview
```

---

## 🚀 Quick Setup & Installation Guide

### 1. Clone or Open Project
```bash
cd pet_care_companion
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-Train ML Models
Both models are pre-trained and included in `ml_models/`. To retrain from scratch:
```bash
python recommendations/train_recommendation_model.py
python breed_detection/train_breed_model.py
```

### 4. Database Setup & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Comprehensive Sample Data
```bash
python manage.py seed_data
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000`** in your browser.

---

## 🗄️ Oracle Database Configuration

To connect directly to an active Oracle Database instance (Oracle XE / Free / 23ai):

1. Follow the steps in [`oracle_sql/oracle_setup_guide.md`](oracle_sql/oracle_setup_guide.md) to create the `pet_care_user` user and tablespace.
2. In your terminal or `.env` file:
   ```bash
   set USE_ORACLE=True
   set ORACLE_DB_USER=pet_care_user
   set ORACLE_DB_PASSWORD=PetCare123#
   set ORACLE_DB_HOST=localhost
   set ORACLE_DB_PORT=1521
   set ORACLE_DB_SERVICE_NAME=FREEPDB1
   ```
3. Run `python manage.py migrate` and `python manage.py seed_data`.
4. Pure Oracle DDL script is available at [`oracle_sql/schema_ddl.sql`](oracle_sql/schema_ddl.sql).

---

## 🚀 Cloud Deployment: Render (Backend & DB) + Vercel (Frontend)

Pet Care Companion is configured for seamless split cloud deployment:
- **Render (`petcare-backend` + `petcare-db`)**: Hosts the Python/Django application, REST APIs, ML inference models, and managed Render PostgreSQL database via `render.yaml` Blueprint.
- **Vercel (`frontend/`)**: Hosts the responsive templates, Three.js 3D assets, custom CSS/JS, and edge rewrites via `frontend/vercel.json`.

👉 **For comprehensive step-by-step instructions, see [`DEPLOYMENT_RENDER_VERCEL.md`](DEPLOYMENT_RENDER_VERCEL.md).**

---

## 🤖 Ollama + Qwen3 4B Local AI Setup

1. Install Ollama from [https://ollama.com](https://ollama.com).
2. Download the Qwen3 4B model:
   ```bash
   ollama run qwen3:4b
   ```
3. Ensure Ollama service is running on default port `11434`.
4. The floating chatbot widget on every page and `/chatbot/` will communicate directly with Ollama.
*(Note: If Ollama is not active, the system automatically uses an intelligent veterinary domain fallback so your demonstration is always 100% functional).*

---

## 🔑 Demo Test Credentials

All sample accounts are seeded via `python manage.py seed_data`:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `Admin123#` | Full Django administration |
| **Pet Owner** | `sarah_jenkins` | `PetOwner123#` | Owns Max (Golden Retriever) & Luna (Persian) |
| **Pet Owner** | `david_miller` | `PetOwner123#` | Owns Rocky (German Shepherd) |
| **Pet Owner** | `priya_sharma` | `PetOwner123#` | Owns Bella (French Bulldog) |
| **Caretaker** | `alex_rivera` | `Caretaker123#` | Top rated sitter ($28/hr) |
| **Caretaker** | `elena_rostova` | `Caretaker123#` | Senior pet specialist ($35/hr) |

---

## 🎓 College Viva / Project Walkthrough Steps

1. **Landing Page**: Showcase responsive UI, 3D particle background, feature breakdown, and global floating chatbot.
2. **Owner Flow**: Log in as `sarah_jenkins`, view dashboard, check **Max's** profile, display the dynamic **QR Pet ID Card**, click Print/PDF, and test the public emergency view.
3. **Health Tracker**: Navigate to Max's health dashboard, view the interactive **Chart.js weight curve**, view upcoming vaccine booster alerts.
4. **Marketplace & Booking**: Search caretakers with filters, book **Alex Rivera** for pet sitting, observe price auto-calculation.
5. **Caretaker Flow**: Log in as `alex_rivera`, view pending booking requests on Caretaker Dashboard, accept the request, and review earnings.
6. **ML Recommendation Feature**: Open `/recommendations/`, select Max or input custom age/weight/activity, generate ML predictions, and explain the Decision Tree/Random Forest multi-target architecture.
7. **ML Breed Detection Feature**: Open `/breed-detection/`, upload a pet image, view predicted breed with confidence percentages and encyclopedia, and click "Use for Recommendations".
8. **AI Chatbot**: Test the bottom-right floating widget on any page or full page at `/chatbot/` asking pet questions ("What foods are toxic for dogs?", "How to potty train a puppy?").
#   p e t c a r e c o m p a n i o n  
 
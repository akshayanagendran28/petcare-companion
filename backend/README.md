# Backend Architecture - Pet Care Companion

The `backend/` directory contains the complete server-side application logic, REST APIs, machine learning pipelines, database interactions, and business services for the **Pet Care Companion** platform.

---

## Directory Structure

```
backend/
├── config/                    # Django Core Configuration
│   ├── settings.py            # Global settings (Oracle / SQLite toggles, Auth, Whitenoise)
│   ├── urls.py                # Master URL routing table
│   ├── wsgi.py                # WSGI entrypoint for production web servers
│   └── asgi.py                # ASGI entrypoint
│
├── users/                     # Custom User model, Authentication & Role-Based Access Control
├── pets/                      # Pet registration, dynamic health metrics & gallery
├── bookings/                  # Caretaker reservations, capacity limit, emergency rush flow & UPI checkout
├── marketplace/               # Caretaker discovery, verified profiles & pricing models
├── adoption/                  # Adoption listings, screening applications & status pipeline
├── health/                    # Medical records, vaccination tracking & vital trend logs
├── lostfound/                 # Community lost & found pet reporting with photo verification
├── matchhub/                  # Pet playdate matchmaking & social networking
├── chatbot/                   # Conversational AI assistant with Ollama LLM integration
├── breed_detection/           # MobileNetV2 ONNX deep-learning breed classification (37+ breeds)
├── recommendations/           # Machine learning pet care service recommendation engine
├── reviews/                   # Caretaker star ratings and verified customer feedback
├── notifications/             # Real-time event notifications & dashboard alerts
│
├── ml/                        # ML training pipelines and feature extractors
├── ml_models/                 # Serialized ONNX, Joblib, and JSON breed/recommendation weights
├── datasets/                  # Oxford Pet dataset and training CSV datasets
│
├── manage.py                  # Backend-specific management utility
├── requirements.txt           # Python backend dependencies
└── README.md                  # This documentation file
```

---

## Core Business Services & Rules

1. **Strict 1-Booking-Per-Day Caretaker Limit:**
   - Enforced in `bookings/utils.py` and `bookings/forms.py`.
   - Prevents caretakers from being overbooked on the same calendar day.

2. **Advance Notice & Emergency Booking Pipeline:**
   - **Standard Bookings:** Require a minimum of 2 days advance notice.
   - **Emergency Bookings:** Supported with minimum 1 hour notice, automatic ₹400 rush fee, and emergency owner contact collection.

3. **UPI Payment Gateway & Verification:**
   - Direct UPI QR Code checkout (GPay, PhonePe, Paytm).
   - Real-time order verification polling via `/bookings/<id>/payment/verify/`.

4. **Deep Learning Breed Classifier:**
   - Uses `mobilenetv2-12.onnx` with ImageNet and Oxford-IIIT Pet Dataset mappings.
   - Accurately classifies 37 pet breeds with detailed care guidelines and temperaments.

---

## Running the Backend

You can manage and run the backend either from the project root or directly from the `backend/` folder:

```bash
# Option 1: Run directly from backend/
cd backend
python manage.py runserver 8000

# Option 2: Run tests
python manage.py test tests_system.PetCareCompanionSystemTest
```

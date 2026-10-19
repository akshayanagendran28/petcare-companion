# Frontend Architecture - Pet Care Companion

The `frontend/` directory encapsulates the complete presentation and user-interface layer of the **Pet Care Companion** platform. It provides a modern, responsive, and mobile-friendly web experience built with Django Templates, Bootstrap 5, FontAwesome 6, and custom vanilla JavaScript for asynchronous interactions.

---

## Directory Structure

```
frontend/
├── templates/                 # Server-rendered HTML5 Django Templates
│   ├── base.html              # Master layout (Navbar, Notification badge, Footer)
│   ├── home.html              # Public landing page & platform highlights
│   ├── adoption/              # Pet adoption listings & adoption request modals
│   ├── bookings/              # Caretaker booking, multi-pet selector & UPI QR checkout
│   ├── breed_detection/       # AI breed classification camera & image upload UI
│   ├── chatbot/               # AI pet assistant conversational interface
│   ├── health/                # Medical history, vaccination schedules & vital logs
│   ├── lostfound/             # Lost & found pet community board with geo-tags
│   ├── marketplace/           # Caretaker search, filtering, and profile showcases
│   ├── matchhub/              # Pet social playdate matchmaking
│   ├── notifications/         # Real-time alert center and booking notifications
│   ├── pets/                  # Pet registration, profile cards & gallery
│   ├── recommendations/       # Machine-learning pet care recommendation cards
│   ├── reviews/               # Star ratings and customer testimonials
│   └── users/                 # Login, Registration, and User Profile Dashboards
│
└── static/                    # Client-side Static Assets
    ├── css/                   # Custom styling, themes & responsive media queries
    ├── js/                    # AJAX polling, QR code status verifier & form handlers
    └── images/                # Default avatars, pet badges, and UI graphic assets
```

---

## Key Frontend Features

1. **Multi-Pet Checkbox Selection:**
   - Allows pet owners to book care for multiple registered pets simultaneously in a single transaction.
   - Dynamic price calculation based on the number of selected pets.

2. **Real-Time Caretaker Availability Calendar:**
   - Visual 14-day availability ribbon showing dates with color-coded status badges.
   - Booked dates are prominently highlighted in **RED** (`Booked`) with 1-booking-per-day enforcement.

3. **Advance & Emergency Booking Flow:**
   - Standard bookings require at least 2 days advance notice.
   - Emergency booking toggle allows same-day/urgent bookings (minimum 1 hour notice) with automatic rush fee (+₹400) calculation and emergency contact detail prompts.

4. **Pure QR Code UPI Payment Interface:**
   - Real-time scannable UPI QR code (GPay, PhonePe, Paytm, BHIM) displayed directly on the checkout page.
   - Asynchronous payment verification polling with instant visual confirmation upon payment success.

5. **AI Breed Detector & Visual Analytics:**
   - Real-time client-side image preview and upload for deep learning breed classification.
   - Interactive charts for pet health metrics (weight trends, vaccination timelines).

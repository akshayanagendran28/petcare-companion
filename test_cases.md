# 🧪 Pet Care Companion — Comprehensive Test Case Document

> **Project:** Pet Care Companion  
> **Total Pages/Endpoints:** 60+  
> **Total Test Cases:** 120+  
> **Date:** 2026-10-18

---

## 1. HOME PAGE (`/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 1.1 | Load home page (unauthenticated) | GET `/` | HTTP 200; renders `home.html` with hero section, features, top caretakers, and testimonials | Public landing page visible without login |
| 1.2 | Home page redirects authenticated user | Login as any user → GET `/` | HTTP 302 → redirect to `/users/dashboard/` | Logged-in users skip landing page and go to dashboard |
| 1.3 | Top caretakers display | GET `/` (at least 1 caretaker with `AVAILABLE` status in DB) | Up to 4 available caretaker cards shown | Shows only caretakers marked as AVAILABLE |
| 1.4 | CSRF cookie is set | GET `/` | Response includes `Set-Cookie: csrftoken=...` | `@ensure_csrf_cookie` decorator ensures token is set |

---

## 2. USER REGISTRATION (`/users/register/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 2.1 | Load registration page | GET `/users/register/` | HTTP 200; renders `users/register.html` with owner and caretaker tabs | Dual-role registration form |
| 2.2 | Register as Pet Owner (valid) | POST with `form_role=owner`, `username=testuser1`, `email=test@mail.com`, `password1=StrongPass123#`, `password2=StrongPass123#`, `first_name=John`, `last_name=Doe` | HTTP 302 → `/users/dashboard/`; user logged in; success message shown | Creates PET_OWNER user, auto-login, and redirects |
| 2.3 | Register as Caretaker (valid) | POST with `form_role=caretaker`, `username=care1`, `email=care@mail.com`, `password1=StrongPass123#`, `password2=StrongPass123#`, `first_name=Jane`, plus caretaker fields (`hourly_rate`, `experience_years`, `services_offered`) | HTTP 302 → `/users/dashboard/`; CaretakerProfile created | Creates CARETAKER user with linked CaretakerProfile |
| 2.4 | Register with mismatched passwords | POST with `password1=Pass123#`, `password2=DifferentPass` | HTTP 200; form re-renders with error "The two password fields didn't match" | Password validation prevents creation |
| 2.5 | Register with duplicate username | POST with existing `username=test_owner` | HTTP 200; form error "A user with that username already exists" | Unique username constraint enforced |
| 2.6 | Register with duplicate email | POST with existing email | HTTP 200; form error about email already in use | Unique email constraint enforced |
| 2.7 | Register with short password | POST with `password1=123`, `password2=123` | HTTP 200; form error "minimum 6 characters" | MinimumLengthValidator (min_length=6) rejects short passwords |
| 2.8 | Redirect if already logged in | Login → GET `/users/register/` | HTTP 302 → `/users/dashboard/` | Authenticated users can't access registration |

---

## 3. USER LOGIN (`/users/login/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 3.1 | Load login page | GET `/users/login/` | HTTP 200; renders `users/login.html` with username/password form | Standard Django login form |
| 3.2 | Login with valid credentials | POST `username=test_owner`, `password=Password123#` | HTTP 302 → `/users/dashboard/`; success message "Welcome back" | Authenticates and redirects |
| 3.3 | Login with email instead of username | POST `username=owner@test.com`, `password=Password123#` | HTTP 302 → `/users/dashboard/` | `EmailOrUsernameModelBackend` supports email login |
| 3.4 | Login with wrong password | POST `username=test_owner`, `password=WrongPass` | HTTP 200; error "Invalid username or password" | Authentication fails gracefully |
| 3.5 | Login with non-existent user | POST `username=nonexistent`, `password=Pass123` | HTTP 200; error "Invalid username or password" | No user found |
| 3.6 | Login with `?next=` redirect | POST to `/users/login/?next=/marketplace/` with valid creds | HTTP 302 → `/marketplace/` | Redirects to the originally requested page |
| 3.7 | Redirect if already logged in | Login → GET `/users/login/` | HTTP 302 → `/users/dashboard/` | Authenticated users skip login page |

---

## 4. USER LOGOUT (`/users/logout/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 4.1 | Logout authenticated user | GET `/users/logout/` | HTTP 302 → `/` (home); message "You have been securely logged out" | Session cleared, redirected to home |
| 4.2 | Logout unauthenticated user | GET `/users/logout/` (not logged in) | HTTP 302 → `/` (home) | No error; graceful redirect |

---

## 5. DASHBOARD ROUTER (`/users/dashboard/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 5.1 | Pet Owner redirected | Login as PET_OWNER → GET `/users/dashboard/` | HTTP 302 → `/users/dashboard/owner/` | Role-based routing for owners |
| 5.2 | Caretaker redirected | Login as CARETAKER → GET `/users/dashboard/` | HTTP 302 → `/users/dashboard/caretaker/` | Role-based routing for caretakers |
| 5.3 | Unauthenticated redirect | GET `/users/dashboard/` (not logged in) | HTTP 302 → `/users/login/?next=/users/dashboard/` | `@login_required` enforced |

---

## 6. PET OWNER DASHBOARD (`/users/dashboard/owner/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 6.1 | Load owner dashboard | Login as owner → GET `/users/dashboard/owner/` | HTTP 200; shows pets count, recent bookings, vaccination reminders, active medicines, notifications | Aggregated owner overview |
| 6.2 | Dashboard with no pets | Login as new owner (0 pets) → GET `/users/dashboard/owner/` | HTTP 200; total_pets = 0; empty state messages | Graceful empty state |
| 6.3 | Dashboard shows upcoming vaccinations | Owner with pet having vaccination due in ≤14 days | Vaccination reminder cards displayed with urgency badges | Filters vaccinations within 14-day window |

---

## 7. CARETAKER DASHBOARD (`/users/dashboard/caretaker/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 7.1 | Load caretaker dashboard | Login as caretaker → GET `/users/dashboard/caretaker/` | HTTP 200; shows pending/upcoming/completed bookings, total earnings, reviews, ML performance prediction | Comprehensive caretaker analytics |
| 7.2 | Pet owner accessing caretaker dashboard | Login as PET_OWNER → GET `/users/dashboard/caretaker/` | HTTP 302 → `/users/dashboard/owner/`; warning message | Access restricted to caretakers |
| 7.3 | Earnings calculation | Caretaker with completed bookings totaling ₹2000 | `total_earnings` = 2000.0 displayed | Sum of completed booking prices |

---

## 8. USER PROFILE (`/users/profile/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 8.1 | Load profile page | Login → GET `/users/profile/` | HTTP 200; user profile form pre-filled with current data | Shows editable user fields |
| 8.2 | Update profile (valid) | POST with updated `first_name=Updated`, `email=new@mail.com` | HTTP 302 → `/users/profile/`; success message "profile updated" | Saves changes to User model |
| 8.3 | Update caretaker profile | Login as caretaker → POST with updated `hourly_rate=300`, `bio=Updated bio` | HTTP 302; both User and CaretakerProfile updated | Dual-form save for caretakers |
| 8.4 | Update with invalid data | POST with `email=invalid-email` | HTTP 200; form error on email field | Validation prevents bad data |

---

## 9. PET LIST (`/pets/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 9.1 | Load pet list | Login as owner with 3 pets → GET `/pets/` | HTTP 200; 3 pet cards displayed | Shows only current user's pets |
| 9.2 | Empty pet list | Login as owner with 0 pets → GET `/pets/` | HTTP 200; empty state / "No pets" message | Graceful empty state |
| 9.3 | Unauthenticated access | GET `/pets/` (not logged in) | HTTP 302 → login page | `@login_required` enforced |

---

## 10. PET CREATE (`/pets/add/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 10.1 | Load add pet form | Login → GET `/pets/add/` | HTTP 200; empty PetForm rendered | Blank form for new pet |
| 10.2 | Pre-fill breed from detection | GET `/pets/add/?breed=Labrador&species=Dog` | Form pre-fills `breed=Labrador`, `species=Dog` | Breed Detection integration |
| 10.3 | Create pet (valid) | POST with `name=Buddy`, `species=Dog`, `breed=Labrador`, `age=3`, `weight=25.5`, `gender=Male` | HTTP 302 → `/pets/<id>/`; success message; QR code auto-generated | Creates pet + generates unique QR Pet ID |
| 10.4 | Create pet with photo | POST with `name=Luna`, multipart image file for `photo` | HTTP 302; pet created with photo saved to `media/pets/` | File upload handling |
| 10.5 | Create pet missing required fields | POST with only `name=Buddy` (missing species, breed) | HTTP 200; form errors on required fields | Validation enforced |

---

## 11. PET DETAIL (`/pets/<id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 11.1 | View own pet detail | Login as owner → GET `/pets/1/` | HTTP 200; full pet profile with QR code, health summary, vaccination history, weight chart, medicines | Complete pet overview |
| 11.2 | View other user's pet | Login as user B → GET `/pets/1/` (owned by user A) | HTTP 403 Forbidden | Permission check: `pet.owner != request.user` |
| 11.3 | Non-existent pet | GET `/pets/99999/` | HTTP 404 Not Found | `get_object_or_404` returns 404 |

---

## 12. PET UPDATE (`/pets/<id>/edit/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 12.1 | Load edit form | Login as owner → GET `/pets/1/edit/` | HTTP 200; PetForm pre-filled with existing pet data | Editable form |
| 12.2 | Update pet (valid) | POST with `name=Buddy Updated`, `weight=26.0` | HTTP 302 → `/pets/1/`; success message | Updates pet record |
| 12.3 | Edit another user's pet | Login as user B → GET `/pets/1/edit/` (owned by user A) | HTTP 404 | Query filters by `owner=request.user` |

---

## 13. PET DELETE (`/pets/<id>/delete/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 13.1 | Load delete confirmation | Login as owner → GET `/pets/1/delete/` | HTTP 200; confirmation page with pet name | Shows "Are you sure?" page |
| 13.2 | Confirm deletion | POST to `/pets/1/delete/` | HTTP 302 → `/pets/`; info message "Pet 'Buddy' was deleted" | Permanently deletes pet record |
| 13.3 | Delete another user's pet | Login as user B → POST `/pets/1/delete/` (owned by user A) | HTTP 404 | Ownership check prevents unauthorized deletion |

---

## 14. PET ID CARD (`/pets/<id>/id-card/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 14.1 | View pet ID card | Login as owner → GET `/pets/1/id-card/` | HTTP 200; printable card with pet photo, QR code, owner contact, breed, vaccinations | Digital pet passport |
| 14.2 | View other user's pet ID card | Login as user B → GET `/pets/1/id-card/` | HTTP 403 Forbidden | Permission restricted |

---

## 15. EMERGENCY PET PROFILE (`/pets/<id>/emergency/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 15.1 | Public emergency profile | GET `/pets/1/emergency/` (no login required) | HTTP 200; shows pet name, breed, owner contact info, medical allergies, emergency instructions | QR code scan target — no login needed |
| 15.2 | Non-existent pet emergency | GET `/pets/99999/emergency/` | HTTP 404 | Pet not found |

---

## 16. MARKETPLACE — CARETAKER LIST (`/marketplace/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 16.1 | Load caretaker marketplace | Login → GET `/marketplace/` | HTTP 200; paginated list of caretaker cards with name, rating, hourly rate, services, avatar | Main caretaker discovery page |
| 16.2 | Search caretakers | GET `/marketplace/?q=Dog Walking` | HTTP 200; filtered results matching "Dog Walking" in services/bio | Full-text Q filter search |
| 16.3 | Filter by min rating | GET `/marketplace/?min_rating=4` | HTTP 200; only caretakers with avg rating ≥ 4.0 | Rating filter |
| 16.4 | Filter by max price | GET `/marketplace/?max_price=200` | HTTP 200; only caretakers with hourly_rate ≤ 200 | Price ceiling filter |
| 16.5 | Sort by rating | GET `/marketplace/?sort=rating_high` | HTTP 200; caretakers sorted by average rating descending | Sort ordering |
| 16.6 | Pagination | GET `/marketplace/?page=2` | HTTP 200; second page of caretaker results | Paginator with page_size |

---

## 17. MARKETPLACE — CARETAKER DETAIL (`/marketplace/<id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 17.1 | View caretaker profile | Login → GET `/marketplace/1/` | HTTP 200; full profile: bio, services, hourly rate, experience, reviews, "Book Now" button | Detailed caretaker page |
| 17.2 | Non-existent caretaker | GET `/marketplace/99999/` | HTTP 404 | Profile not found |

---

## 18. BOOKING — CREATE BOOKING (`/bookings/create/<caretaker_id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 18.1 | Load booking form | Login as owner → GET `/bookings/create/1/` | HTTP 200; form with pet checkboxes, service type, date range picker, availability calendar ribbon, emergency toggle | Booking creation page |
| 18.2 | Create standard booking (valid) | POST with `pets=[1,2]`, `service_type=Pet Sitting`, `start_date=<today+3>`, `end_date=<today+4>`, `start_time=09:00 AM`, `end_time=05:00 PM` | HTTP 302 → `/bookings/<id>/payment/`; booking created with status=PENDING, payment_status=UNPAID | Multi-pet standard booking |
| 18.3 | Book own services | Login as caretaker → GET `/bookings/create/<own_id>/` | HTTP 302 → caretaker detail; error "You cannot book your own services" | Self-booking prevention |
| 18.4 | Booking date in past | POST with `start_date=<yesterday>` | HTTP 200; form error "Start date cannot be in the past" | Past date validation |
| 18.5 | End date before start date | POST with `start_date=<date>`, `end_date=<date-1>` | HTTP 200; form error "End date must be on or after start date" | Date range validation |
| 18.6 | Standard booking < 2 days advance | POST with `start_date=<tomorrow>` (non-emergency) | HTTP 200; error "Standard bookings must be made at least 2 days in advance" | 2-day advance notice rule |
| 18.7 | Emergency booking (valid) | POST with `is_emergency=True`, `start_date=<today>`, `emergency_phone=9876543210`, `emergency_reason=Pet injured`, `arrival_time=<now+2hrs>` | HTTP 302 → payment; `emergency_fee=400.00` added to total_price | Emergency flow with ₹400 surcharge |
| 18.8 | Emergency booking missing phone | POST with `is_emergency=True`, `emergency_phone=` (blank) | HTTP 200; error "Please provide an emergency contact number" | Emergency fields required |
| 18.9 | Emergency booking < 1hr notice | POST with `is_emergency=True`, `start_date=today`, `arrival_time=<now+30min>` | HTTP 200; error "must be scheduled at least 1 hour in advance" | 1-hour minimum notice for emergencies |
| 18.10 | Caretaker already booked that day | First booking accepted for `date X` → POST 2nd booking for same caretaker on `date X` | HTTP 200; error "maximum of 1 booking per day" | 1-booking/day capacity limit |
| 18.11 | No pets selected | POST without selecting any pet | HTTP 200; form error "Please choose at least one pet" | At least one pet required |
| 18.12 | Price calculation | 2 pets × 3 days × 4hrs/day × ₹200/hr rate | `total_price = 2 × 3 × 4 × 200 = ₹4,800.00` | Multi-pet price formula |

---

## 19. BOOKING — AVAILABILITY API (`/bookings/api/availability/<caretaker_id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 19.1 | Get availability data | Login → GET `/bookings/api/availability/1/` | HTTP 200; JSON with `unavailable_dates` array, `today_count`, `max_capacity`, `next_available_date` | Dynamic calendar data for frontend |
| 19.2 | Booked dates included | Caretaker has accepted booking on `2026-11-01` | JSON `unavailable_dates` contains `"2026-11-01"` | Fully booked dates highlighted |

---

## 20. BOOKING — OWNER BOOKING LIST (`/bookings/my-bookings/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 20.1 | View all bookings | Login as owner → GET `/bookings/my-bookings/` | HTTP 200; list of all bookings with caretaker name, pet, dates, status, price | Owner's booking history |
| 20.2 | Filter by status | GET `/bookings/my-bookings/?status=PENDING` | HTTP 200; only PENDING bookings shown | Status filter |
| 20.3 | No bookings | Login as new owner → GET `/bookings/my-bookings/` | HTTP 200; empty state | Graceful empty state |

---

## 21. BOOKING — CARETAKER REQUESTS (`/bookings/caretaker/requests/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 21.1 | View incoming requests | Login as caretaker → GET `/bookings/caretaker/requests/` | HTTP 200; list of all bookings assigned to this caretaker | Caretaker's inbox |
| 21.2 | Pet owner accessing | Login as PET_OWNER → GET `/bookings/caretaker/requests/` | HTTP 403 Forbidden | Role restriction enforced |
| 21.3 | Filter by status | GET `/bookings/caretaker/requests/?status=ACCEPTED` | HTTP 200; only ACCEPTED bookings | Status filter |

---

## 22. BOOKING — UPDATE STATUS (`/bookings/<id>/<action>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 22.1 | Accept booking | Login as caretaker → GET `/bookings/1/accept/` | HTTP 302; booking.status → `ACCEPTED`; notification sent to owner | Caretaker confirms booking |
| 22.2 | Reject booking | Login as caretaker → GET `/bookings/1/reject/` | HTTP 302; booking.status → `REJECTED`; notification sent to owner | Caretaker declines booking |
| 22.3 | Complete booking | Login as caretaker → GET `/bookings/1/complete/` | HTTP 302; booking.status → `COMPLETED`; earnings updated; review notification sent | Marks service delivered |
| 22.4 | Cancel booking (owner) | Login as owner → GET `/bookings/1/cancel/` | HTTP 302; booking.status → `CANCELLED`; notification sent to caretaker | Owner cancels booking |
| 22.5 | Unauthorized status update | Login as random user → GET `/bookings/1/accept/` | HTTP 403 Forbidden | Permission check fails |

---

## 23. BOOKING — PAYMENT PAGE (`/bookings/<id>/payment/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 23.1 | Payment locked (PENDING) | Booking status=PENDING → GET `/bookings/1/payment/` | HTTP 200; page shows `is_locked=True`; "Waiting for caretaker to accept" message | Payment unlocked only after ACCEPTED |
| 23.2 | Payment unlocked (ACCEPTED) | Booking status=ACCEPTED → GET `/bookings/1/payment/` | HTTP 200; UPI QR code displayed, Razorpay order created, "Pay Now" button visible | Ready for payment |
| 23.3 | Payment already completed | Booking `payment_status=PAID` → GET `/bookings/1/payment/` | HTTP 200; shows payment receipt with `is_paid=True`, transaction ID, paid timestamp | Confirmed payment receipt |
| 23.4 | Unauthorized access | Login as random user → GET `/bookings/1/payment/` | HTTP 403 Forbidden | Only owner, caretaker, or admin |

---

## 24. BOOKING — VERIFY PAYMENT API (`/bookings/<id>/payment/verify/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 24.1 | UPI/GPay direct verification | POST JSON `{"upi_direct": true}` | HTTP 200; JSON `{"status":"success"}`, booking.payment_status → `PAID`, auto-generated UTR | Real-time UPI scan confirmation |
| 24.2 | UPI with valid UTR | POST JSON `{"utr_number": "123456789012"}` | HTTP 200; payment recorded with given UTR, status=SUCCESS | Manual UTR entry verification |
| 24.3 | UPI with short UTR | POST JSON `{"utr_number": "123"}` | HTTP 400; error "Please enter a valid 12-digit UPI Reference" | UTR length validation |
| 24.4 | Duplicate UTR across bookings | POST JSON `{"utr_number": "<already-used-utr>"}` | HTTP 400; error "This UPI Reference ID has already been used" | Duplicate UTR prevention |
| 24.5 | Razorpay signature verification | POST JSON `{"razorpay_order_id":"order_x", "razorpay_payment_id":"pay_x", "razorpay_signature":"<valid_hmac>"}` | HTTP 200; JSON `{"status":"success"}` | HMAC-SHA256 signature validates |
| 24.6 | Razorpay invalid signature | POST with wrong `razorpay_signature` | HTTP 400; error message | Signature mismatch rejection |
| 24.7 | Missing payment fields | POST JSON `{}` | HTTP 400; error "Missing payment verification credentials" | Required fields check |
| 24.8 | GET request (wrong method) | GET `/bookings/1/payment/verify/` | HTTP 405; error "POST method required" | Only POST allowed |

---

## 25. BOOKING — PAYMENT STATUS API (`/bookings/<id>/payment/status/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 25.1 | Check unpaid status | GET (booking unpaid) | HTTP 200; JSON `{"is_paid": false, "payment_status": "UNPAID"}` | Polling endpoint for QR scan |
| 25.2 | Check paid status | GET (booking paid) | HTTP 200; JSON `{"is_paid": true, "payment_status": "PAID"}` | Confirms payment completed |

---

## 26. BOOKING — PAYMENT FAILED API (`/bookings/<id>/payment/failed/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 26.1 | Record payment failure | POST JSON `{"error_code":"PAYMENT_CANCELLED", "error_description":"User cancelled"}` | HTTP 200; JSON `{"status":"recorded"}`; failure logged in Payment model | Failure audit trail |

---

## 27. REVIEWS — CREATE REVIEW (`/reviews/add/<booking_id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 27.1 | Load review form | Login as owner → GET `/reviews/add/1/` (booking status=COMPLETED) | HTTP 200; ReviewForm with star rating (1-5) and comment textarea | Review form for completed bookings |
| 27.2 | Submit review (valid) | POST with `rating=5`, `comment=Excellent service!` | HTTP 302; Review created; caretaker avg rating recalculated | Saves review linked to booking & caretaker |
| 27.3 | Review non-completed booking | GET `/reviews/add/1/` (booking status=PENDING) | HTTP 302 or error message | Only COMPLETED bookings can be reviewed |
| 27.4 | Non-owner reviewing | Login as user B → GET `/reviews/add/1/` (owned by user A) | HTTP 403 Forbidden | Only booking owner can review |

---

## 28. ADOPTION — LISTING LIST (`/adoption/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 28.1 | Load adoption catalog | Login → GET `/adoption/` | HTTP 200; paginated grid of ACTIVE adoption/sale listings | Adoption marketplace page |
| 28.2 | Search by pet name | GET `/adoption/?q=Buddy` | HTTP 200; filtered results matching "Buddy" in name/breed/location/description | Full-text search |
| 28.3 | Filter by species | GET `/adoption/?species=Cat` | HTTP 200; only cat listings | Species filter |
| 28.4 | Filter by listing type | GET `/adoption/?type=ADOPTION` | HTTP 200; only free adoption listings | Adoption vs Sale toggle |
| 28.5 | Filter by gender | GET `/adoption/?gender=Male` | HTTP 200; only male pet listings | Gender filter |
| 28.6 | Filter by max price | GET `/adoption/?max_price=500` | HTTP 200; only listings with price ≤ ₹500 | Price ceiling |
| 28.7 | Sort by price low | GET `/adoption/?sort=price_low` | HTTP 200; listings sorted by price ascending | Sort ordering |
| 28.8 | Pagination | GET `/adoption/?page=2` | HTTP 200; page 2 of 9-per-page results | Paginator |

---

## 29. ADOPTION — LISTING DETAIL (`/adoption/<id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 29.1 | View listing detail | GET `/adoption/1/` | HTTP 200; pet name, species, breed, age, gender, price, owner contact, related listings, adoption inquiry form | Full listing page |
| 29.2 | Owner sees incoming requests | Login as listing owner → GET `/adoption/1/` | HTTP 200; shows list of AdoptionRequest entries from applicants | Owner management view |
| 29.3 | Applicant sees own request status | Login as applicant → GET `/adoption/1/` (after submitting inquiry) | HTTP 200; shows `user_request` status (PENDING/ACCEPTED/REJECTED) | Request tracking |

---

## 30. ADOPTION — CREATE LISTING (`/adoption/add/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 30.1 | Load creation form | Login → GET `/adoption/add/` | HTTP 200; AdoptionListingForm with pre-filled contact info from user profile | Pre-populated form |
| 30.2 | Create listing (valid) | POST with `pet_name=Milo`, `species=Dog`, `breed=Beagle`, `age=2`, `gender=Male`, `listing_type=ADOPTION`, `price=0`, `description=Friendly`, `location=Chennai` | HTTP 302 → `/adoption/<id>/`; listing status=ACTIVE | New listing published |
| 30.3 | Create listing missing fields | POST with only `pet_name=Milo` | HTTP 200; form validation errors | Required fields enforced |

---

## 31. ADOPTION — MY LISTINGS (`/adoption/my-listings/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 31.1 | View own listings | Login → GET `/adoption/my-listings/` | HTTP 200; all listings created by current user (ACTIVE, CLOSED, ADOPTED) | Personal listing management |

---

## 32. ADOPTION — SUBMIT INQUIRY (`/adoption/<id>/inquire/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 32.1 | Submit adoption inquiry | POST with `applicant_name`, `applicant_phone`, `housing_type`, `pet_experience`, `message` | HTTP 302 → listing detail; AdoptionRequest created; notification sent to owner | Adoption application submitted |
| 32.2 | Inquire own listing | Login as listing owner → POST `/adoption/1/inquire/` | HTTP 302; warning "cannot submit adoption application for your own pet" | Self-inquiry prevention |
| 32.3 | Update existing inquiry | Submit 2nd inquiry on same listing | AdoptionRequest updated (not duplicated) via `update_or_create` | Upsert logic |

---

## 33. ADOPTION — HANDLE REQUEST (`/adoption/requests/<request_id>/<action>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 33.1 | Accept adoption request | Login as owner → GET `.../accept/` | HTTP 302; request status → ACCEPTED; payment unlocked for applicant | Owner approves applicant |
| 33.2 | Reject adoption request | Login as owner → GET `.../reject/` | HTTP 302; request status → REJECTED | Owner rejects applicant |

---

## 34. ADOPTION — PAYMENT & VERIFICATION (`/adoption/<id>/payment/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 34.1 | Payment locked (not accepted) | GET (request not accepted) | HTTP 200; payment locked message | Payment only unlocked after request acceptance |
| 34.2 | Payment unlocked | GET (request accepted) | HTTP 200; UPI QR code + Razorpay order shown | Ready for payment |
| 34.3 | Verify adoption payment | POST to `/adoption/1/payment/verify/` with valid data | HTTP 200; payment confirmed; listing status → ADOPTED | Adoption payment flow |
| 34.4 | Check payment status | GET `/adoption/1/payment/status/` | HTTP 200; JSON with `is_paid` boolean | Polling endpoint |

---

## 35. ADOPTION — UPDATE LISTING STATUS (`/adoption/<id>/status/<new_status>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 35.1 | Close listing | Login as owner → GET `/adoption/1/status/CLOSED/` | HTTP 302; listing.status → CLOSED | Owner removes listing |
| 35.2 | Reactivate listing | GET `/adoption/1/status/ACTIVE/` | HTTP 302; listing.status → ACTIVE | Owner re-publishes |

---

## 36. HEALTH — DASHBOARD (`/health/<pet_id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 36.1 | Load health dashboard | Login as pet owner → GET `/health/1/` | HTTP 200; vaccination timeline, medical records, weight chart (Chart.js), active medicines, allergies | Complete pet health view |
| 36.2 | Access another owner's pet health | Login as user B → GET `/health/1/` (pet owned by user A) | HTTP 403 Forbidden | Permission enforced |
| 36.3 | Non-existent pet | GET `/health/99999/` | HTTP 404 | Pet not found |

---

## 37. HEALTH — ADD RECORD (`/health/<pet_id>/add/<record_type>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 37.1 | Add vaccination record | POST to `/health/1/add/vaccination/` with `vaccine_name=Rabies`, `administered_date=2026-10-01`, `next_due_date=2027-10-01` | HTTP 302 → health dashboard; vaccination saved | New vaccination entry |
| 37.2 | Add medical record | POST to `/health/1/add/medical/` with `condition=Ear Infection`, `diagnosis=Otitis`, `treatment=Antibiotics` | HTTP 302; HealthRecord created | Medical history entry |
| 37.3 | Add medicine record | POST to `/health/1/add/medicine/` with `medicine_name=Amoxicillin`, `dosage=250mg`, `start_date`, `end_date`, `is_active=True` | HTTP 302; MedicineRecord created | Active prescription |
| 37.4 | Add weight record | POST to `/health/1/add/weight/` with `weight_kg=12.5`, `recorded_date=2026-10-18` | HTTP 302; WeightRecord created | Weight tracking point |
| 37.5 | Add allergy record | POST to `/health/1/add/allergy/` with `allergen=Chicken`, `severity=Moderate`, `reaction=Skin rash` | HTTP 302; AllergyRecord created | Allergy registry |
| 37.6 | Invalid record type | GET `/health/1/add/invalid_type/` | HTTP 400 or redirect with error | Unknown record type rejected |

---

## 38. HEALTH — WEIGHT DATA API (`/health/<pet_id>/weight-data/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 38.1 | Get weight time series | Login → GET `/health/1/weight-data/` | HTTP 200; JSON array with `[{date, weight_kg}, ...]` | Chart.js data source |
| 38.2 | Empty weight history | GET (pet with 0 weight records) | HTTP 200; JSON empty array `[]` | Graceful empty response |

---

## 39. HEALTH — ADD WEIGHT AJAX (`/health/<pet_id>/add-weight-ajax/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 39.1 | AJAX weight entry | POST JSON `{"weight_kg": 13.2, "recorded_date": "2026-10-18"}` | HTTP 200; JSON `{"status":"success"}` | Real-time weight logging via AJAX |
| 39.2 | Invalid weight value | POST JSON `{"weight_kg": -5}` | HTTP 400; validation error | Negative weight rejected |

---

## 40. HEALTH — REMINDERS (`/health/reminders/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 40.1 | View vaccination reminders | Login → GET `/health/reminders/` | HTTP 200; upcoming vaccinations within 14 days with urgency badges (Due Soon / Overdue) | Preventive care alerts |

---

## 41. BREED DETECTION (`/breed-detection/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 41.1 | Load breed detection page | Login → GET `/breed-detection/` | HTTP 200; image upload form with camera/file picker | AI breed classifier UI |
| 41.2 | Classify dog breed | POST multipart with dog image file | HTTP 200; top-3 breed predictions with confidence %, breed details, care guidelines, "Register this breed" link | MobileNetV2 ONNX inference |
| 41.3 | Classify cat breed | POST multipart with cat image file | HTTP 200; cat breed prediction results | Supports 37+ breeds (dogs + cats) |
| 41.4 | Non-pet image | POST with image of car/building | HTTP 200; low-confidence results or "Could not confidently identify breed" message | Graceful handling of non-pet images |
| 41.5 | No image uploaded | POST without file | HTTP 200; form error "Please upload an image" | Required file validation |

---

## 42. CHATBOT — PAGE (`/chatbot/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 42.1 | Load chatbot page | Login → GET `/chatbot/` | HTTP 200; dedicated chat interface with message history, input box | Full-page AI assistant |

---

## 43. CHATBOT — CHAT API (`/chatbot/api/chat/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 43.1 | Send chat message | POST JSON `{"message": "What vaccinations does a puppy need?"}` | HTTP 200; JSON with AI response text | Ollama LLM integration with domain fallback |
| 43.2 | Empty message | POST JSON `{"message": ""}` | HTTP 400 or default response | Empty input handling |
| 43.3 | Chat history stored | Send 3 messages → GET `/chatbot/api/history/` | HTTP 200; JSON array with 3 Q&A pairs | ChatHistory model persistence |

---

## 44. CHATBOT — HISTORY API (`/chatbot/api/history/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 44.1 | Get full chat history | Login → GET `/chatbot/api/history/` | HTTP 200; JSON array of all user's chat messages | Paginated history retrieval |
| 44.2 | New user (no history) | Login as new user → GET `/chatbot/api/history/` | HTTP 200; JSON empty array | Graceful empty state |

---

## 45. CHATBOT — CLEAR HISTORY (`/chatbot/api/clear/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 45.1 | Clear all chat history | POST `/chatbot/api/clear/` | HTTP 200; all ChatHistory records for user deleted | Clean slate for conversation |

---

## 46. RECOMMENDATIONS (`/recommendations/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 46.1 | Load recommendations page | Login as owner with pets → GET `/recommendations/` | HTTP 200; ML-generated care recommendations per pet (diet, exercise, compatible caretakers, tips) | Random Forest model predictions |
| 46.2 | No pets registered | Login as owner with 0 pets → GET `/recommendations/` | HTTP 200; message to register pets first | Empty state guidance |
| 46.3 | Recommendation logging | View recommendations | RecommendationLog entry created with model version and features | Audit trail |

---

## 47. LOST & FOUND — LIST (`/lostfound/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 47.1 | Load lost pets list | Login → GET `/lostfound/` | HTTP 200; grid of lost pet reports with photos, last seen location, status (MISSING/FOUND/REUNITED) | Community board |
| 47.2 | Search lost pets | GET `/lostfound/?q=Labrador` | HTTP 200; filtered results | Search filter |

---

## 48. LOST & FOUND — REPORT (`/lostfound/report/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 48.1 | Load report form | Login → GET `/lostfound/report/` | HTTP 200; LostPetReportForm | Report submission form |
| 48.2 | Submit report (valid) | POST with `pet_name=Max`, `species=Dog`, `last_seen_location=Central Park`, `last_seen_date`, `description`, `photo`, `contact_phone` | HTTP 302 → report detail; LostPetReport created | Creates missing pet alert |
| 48.3 | Missing required fields | POST without `pet_name` | HTTP 200; form errors | Validation enforced |

---

## 49. LOST & FOUND — DETAIL (`/lostfound/<id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 49.1 | View report detail | Login → GET `/lostfound/1/` | HTTP 200; full report with photo, map location, sighting list, "Submit Sighting" form | Report detail page |
| 49.2 | Non-existent report | GET `/lostfound/99999/` | HTTP 404 | Report not found |

---

## 50. LOST & FOUND — EDIT REPORT (`/lostfound/<id>/edit/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 50.1 | Edit own report | Login as reporter → POST with updated fields | HTTP 302; report updated | Owner can edit |
| 50.2 | Edit another user's report | Login as user B → GET `/lostfound/1/edit/` | HTTP 403 | Ownership check |

---

## 51. LOST & FOUND — SUBMIT SIGHTING (`/lostfound/<id>/sighting/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 51.1 | Submit sighting | POST with `location=Near Park`, `description=Saw matching dog`, `sighting_date`, `photo` | HTTP 302; LostPetSighting created; notification sent to reporter | Community sighting |

---

## 52. LOST & FOUND — MARK REUNITED (`/lostfound/<id>/reunited/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 52.1 | Mark as reunited | Login as reporter → POST `/lostfound/1/reunited/` | HTTP 302; report.status → REUNITED | Owner confirms pet found |

---

## 53. LOST & FOUND — VERIFY POLICE DOCUMENT (`/lostfound/<id>/verify-police-doc/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 53.1 | Upload police document | POST multipart with police FIR/complaint document | HTTP 200; JSON success; document verified | Police report verification AJAX |

---

## 54. MATCH HUB — LIST (`/matchhub/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 54.1 | Load match profiles | Login → GET `/matchhub/` | HTTP 200; grid of pet profiles available for playdates/matching | Pet companion discovery |
| 54.2 | Search/filter matches | GET `/matchhub/?q=Labrador` | HTTP 200; filtered profiles | Search by breed/name |

---

## 55. MATCH HUB — CREATE PROFILE (`/matchhub/add-profile/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 55.1 | Create match profile | POST with `pet` selection, `match_type=PLAYDATE`, `description`, `location` | HTTP 302; MatchProfile created | Registers pet for matching |

---

## 56. MATCH HUB — SEND REQUEST (`/matchhub/request/<receiver_id>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 56.1 | Send match request | POST `/matchhub/request/2/` with `message` | HTTP 302; MatchRequest created; notification sent | Playdate request |
| 56.2 | Self-request prevention | POST `/matchhub/request/<own_id>/` | HTTP 302; error message | Can't request own profile |

---

## 57. MATCH HUB — REQUESTS INBOX (`/matchhub/requests/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 57.1 | View match requests | Login → GET `/matchhub/requests/` | HTTP 200; incoming and outgoing match requests with statuses | Request management |

---

## 58. MATCH HUB — UPDATE REQUEST STATUS (`/matchhub/requests/<id>/<action>/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 58.1 | Accept match request | GET `/matchhub/requests/1/accept/` | HTTP 302; request.status → ACCEPTED; notification sent | Confirms playdate |
| 58.2 | Reject match request | GET `/matchhub/requests/1/reject/` | HTTP 302; request.status → REJECTED | Declines playdate |

---

## 59. NOTIFICATIONS — LIST (`/notifications/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 59.1 | Load notifications | Login → GET `/notifications/` | HTTP 200; list of all notifications ordered by newest first | Notification center |
| 59.2 | No notifications | Login as new user → GET `/notifications/` | HTTP 200; empty state | Graceful empty state |

---

## 60. NOTIFICATIONS — MARK AS READ (`/notifications/<id>/read/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 60.1 | Mark single notification read | POST `/notifications/1/read/` | HTTP 302; notification.is_read = True | Read status toggle |

---

## 61. NOTIFICATIONS — MARK ALL READ (`/notifications/read-all/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 61.1 | Mark all as read | POST `/notifications/read-all/` | HTTP 302; all user notifications marked as read | Bulk read action |

---

## 62. NOTIFICATIONS — UNREAD COUNT API (`/notifications/api/unread-count/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 62.1 | Get unread count | GET `/notifications/api/unread-count/` | HTTP 200; JSON `{"unread_count": 5}` | Navbar badge data source |
| 62.2 | Zero unread | GET (all read) | HTTP 200; JSON `{"unread_count": 0}` | Clean badge state |

---

## 63. DJANGO ADMIN (`/admin/`)

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| 63.1 | Load admin login | GET `/admin/` | HTTP 200 or 302 → admin login | Django built-in admin interface |
| 63.2 | Admin with superuser | Login as superuser → GET `/admin/` | HTTP 200; Django admin dashboard with all models | Full model management |

---

## CROSS-CUTTING TEST CASES

| # | Test Case | Input | Expected Output | Explanation |
|---|-----------|-------|-----------------|-------------|
| CC.1 | CSRF protection on all POST forms | POST without CSRF token | HTTP 403 "CSRF verification failed" | Django CSRF middleware active |
| CC.2 | Static files serving | GET `/static/css/custom.css` | HTTP 200; CSS content served | Whitenoise / Django staticfiles |
| CC.3 | Media files serving | GET `/media/pets/photo.jpg` | HTTP 200; image served | Django media handler (DEBUG mode) |
| CC.4 | 404 for invalid URL | GET `/nonexistent-page/` | HTTP 404 | Django default 404 handler |
| CC.5 | Notification badge on every page | Load any authenticated page | Navbar shows unread notification count | `notification_badge` context processor |
| CC.6 | Mobile responsive layout | Load any page on mobile viewport (375px) | Content adapts; no horizontal scroll; menus collapse | Bootstrap 5 responsive grid |
| CC.7 | Session persistence | Login → close tab → reopen → navigate to `/users/dashboard/` | Still logged in; dashboard loads | Django session cookie |
| CC.8 | QR code generation on pet create | Create new pet | `pet.qr_code` field populated with valid QR image path | Auto-generated in Pet model save |
| CC.9 | Concurrent booking prevention | Two users simultaneously book same caretaker for same date → second submit | Second booking rejected with "already booked on [date]" | Race condition handled by capacity validation |
| CC.10 | Emergency fee calculation | Emergency booking: 2 pets × 3 days × 4hrs × ₹200/hr + ₹400 surcharge | total_price = ₹4,800 + ₹400 = ₹5,200 | Emergency surcharge added correctly |

---

> **Total Test Cases: 126**  
> Covers all 14 Django apps, 60+ URL endpoints, authentication, authorization, form validations, API endpoints, payment flows, ML inference, and cross-cutting concerns.

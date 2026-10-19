CREATE TABLE "ADOPTION_LISTINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "age" decimal NOT NULL, "gender" varchar(10) NOT NULL, "listing_type" varchar(20) NOT NULL, "price" decimal NOT NULL, "location" varchar(200) NOT NULL, "vaccination_status" varchar(50) NOT NULL, "description" text NOT NULL, "photo" varchar(100) NULL, "contact_phone" varchar(20) NOT NULL, "contact_email" varchar(254) NOT NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "adopter_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_status" varchar(20) NOT NULL);

CREATE TABLE "ADOPTION_PAYMENTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "razorpay_order_id" varchar(100) NOT NULL UNIQUE, "razorpay_payment_id" varchar(100) NULL, "razorpay_signature" varchar(255) NULL, "amount" decimal NOT NULL, "currency" varchar(10) NOT NULL, "status" varchar(20) NOT NULL, "payment_method" varchar(60) NOT NULL, "error_code" varchar(100) NULL, "error_description" text NULL, "paid_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "adopter_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "listing_id" bigint NOT NULL REFERENCES "ADOPTION_LISTINGS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "ADOPTION_REQUESTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "applicant_name" varchar(120) NOT NULL, "applicant_email" varchar(254) NOT NULL, "applicant_phone" varchar(30) NOT NULL, "housing_type" varchar(100) NOT NULL, "pet_experience" varchar(100) NOT NULL, "message" text NOT NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "applicant_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "listing_id" bigint NOT NULL REFERENCES "ADOPTION_LISTINGS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "ALLERGIES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "allergy_name" varchar(150) NOT NULL, "severity" varchar(20) NOT NULL, "notes" text NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "BOOKINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "service_type" varchar(100) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "start_time" varchar(10) NOT NULL, "end_time" varchar(10) NOT NULL, "total_price" decimal NOT NULL, "notes" text NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "caretaker_id" bigint NOT NULL REFERENCES "CARETAKERS" ("id") DEFERRABLE INITIALLY DEFERRED, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_status" varchar(20) NOT NULL, "arrival_time" varchar(20) NULL, "emergency_fee" decimal NOT NULL, "emergency_phone" varchar(20) NULL, "emergency_reason" text NULL, "is_emergency" bool NOT NULL);

CREATE TABLE "BOOKINGS_pets" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking_id" bigint NOT NULL REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "BREED_SCANS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "predicted_breed" varchar(100) NOT NULL, "confidence_score" decimal NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "CARETAKERS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "experience_years" decimal NOT NULL, "hourly_rate" decimal NOT NULL, "services_offered" varchar(500) NOT NULL, "availability_status" varchar(20) NOT NULL, "bio" text NULL, "rating" decimal NOT NULL, "total_reviews" integer unsigned NOT NULL CHECK ("total_reviews" >= 0), "total_earnings" decimal NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "CHAT_HISTORY" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "session_id" varchar(100) NOT NULL, "user_query" text NOT NULL, "bot_response" text NOT NULL, "model_used" varchar(50) NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "HEALTH_RECORDS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "record_date" date NOT NULL, "condition_title" varchar(200) NOT NULL, "diagnosis" text NULL, "treatment_plan" text NULL, "vet_name" varchar(150) NULL, "clinic_name" varchar(200) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "LOST_PETS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "last_seen_location" varchar(255) NOT NULL, "date_lost" date NOT NULL, "description" text NULL, "contact_number" varchar(30) NOT NULL, "photo" varchar(100) NULL, "reward_amount" decimal NOT NULL, "status" varchar(25) NOT NULL, "created_at" datetime NOT NULL, "reporter_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "alternate_contact" varchar(50) NULL, "approx_age" varchar(50) NULL, "collar_description" varchar(200) NULL, "color_pattern" varchar(150) NULL, "contact_name" varchar(150) NULL, "distinctive_marks" text NULL, "gender" varchar(15) NOT NULL, "how_lost" text NULL, "microchip_id" varchar(100) NULL, "police_complaint_status" varchar(30) NOT NULL, "police_contact_details" varchar(200) NULL, "police_csr_number" varchar(100) NULL, "police_filing_date" date NULL, "police_station_name" varchar(200) NULL, "reunited_date" date NULL, "reunited_details" text NULL, "reward_details" varchar(255) NULL, "time_lost" varchar(100) NULL, "updated_at" datetime NOT NULL, "police_document" varchar(100) NULL, "police_verification_confidence" decimal NOT NULL, "police_verification_details" text NULL, "police_verified_at" datetime NULL, "police_verified_by_ai" bool NOT NULL);

CREATE TABLE "LOST_PET_SIGHTINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "reporter_name" varchar(150) NOT NULL, "reporter_contact" varchar(100) NOT NULL, "sighting_location" varchar(255) NOT NULL, "sighting_date" date NOT NULL, "description" text NOT NULL, "photo" varchar(100) NULL, "created_at" datetime NOT NULL, "lost_pet_id" bigint NOT NULL REFERENCES "LOST_PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "sighting_time" varchar(50) NULL);

CREATE TABLE "MATCH_PROFILES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bio" text NOT NULL, "looking_for" varchar(100) NOT NULL, "location" varchar(200) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL UNIQUE REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "MATCH_REQUESTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "message" varchar(500) NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "receiver_profile_id" bigint NOT NULL REFERENCES "MATCH_PROFILES" ("id") DEFERRABLE INITIALLY DEFERRED, "sender_profile_id" bigint NOT NULL REFERENCES "MATCH_PROFILES" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "MEDICINES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "medicine_name" varchar(150) NOT NULL, "dosage" varchar(100) NOT NULL, "frequency" varchar(100) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "notes" text NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "NOTIFICATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(150) NOT NULL, "message" varchar(500) NOT NULL, "notification_type" varchar(30) NOT NULL, "link" varchar(255) NULL, "is_read" bool NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "PAYMENTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "razorpay_order_id" varchar(100) NULL, "razorpay_payment_id" varchar(100) NULL, "razorpay_signature" varchar(255) NULL, "amount" decimal NOT NULL, "currency" varchar(10) NOT NULL, "status" varchar(20) NOT NULL, "payment_method" varchar(50) NULL, "bank_transaction_id" varchar(100) NULL, "error_code" varchar(100) NULL, "error_description" text NULL, "paid_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "booking_id" bigint NOT NULL UNIQUE REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "PETS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "age" decimal NOT NULL, "gender" varchar(10) NOT NULL, "weight" decimal NOT NULL, "health_condition" varchar(100) NOT NULL, "activity_level" varchar(20) NOT NULL, "vaccination_status" varchar(20) NOT NULL, "allergies" varchar(255) NULL, "medical_notes" text NULL, "photo" varchar(100) NULL, "qr_code" varchar(100) NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "RECOMMENDATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "input_breed" varchar(100) NOT NULL, "input_age" decimal NOT NULL, "input_weight" decimal NOT NULL, "input_health" varchar(100) NOT NULL, "input_activity" varchar(50) NOT NULL, "diet_category" varchar(150) NOT NULL, "recommended_food" varchar(200) NOT NULL, "recommended_service" varchar(200) NOT NULL, "care_tip" text NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "REVIEWS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), "comment" text NOT NULL, "created_at" datetime NOT NULL, "booking_id" bigint NOT NULL UNIQUE REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED, "caretaker_id" bigint NOT NULL REFERENCES "CARETAKERS" ("id") DEFERRABLE INITIALLY DEFERRED, "reviewer_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "USERS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "role" varchar(20) NOT NULL, "phone" varchar(20) NULL, "address" varchar(255) NULL, "profile_photo" varchar(100) NULL);

CREATE TABLE "USERS_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "USERS_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "VACCINATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "vaccine_name" varchar(150) NOT NULL, "administered_date" date NOT NULL, "next_due_date" date NOT NULL, "batch_number" varchar(50) NULL, "vet_name" varchar(150) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "WEIGHT_HISTORY" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "recorded_date" date NOT NULL, "weight_kg" decimal NOT NULL, "notes" varchar(255) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE UNIQUE INDEX "USERS_groups_user_id_group_id_f430ea61_uniq" ON "USERS_groups" ("user_id", "group_id");

CREATE INDEX "USERS_groups_user_id_b5eb2d31" ON "USERS_groups" ("user_id");

CREATE INDEX "USERS_groups_group_id_7d78bea2" ON "USERS_groups" ("group_id");

CREATE UNIQUE INDEX "USERS_user_permissions_user_id_permission_id_334f28e0_uniq" ON "USERS_user_permissions" ("user_id", "permission_id");

CREATE INDEX "USERS_user_permissions_user_id_9a604f02" ON "USERS_user_permissions" ("user_id");

CREATE INDEX "USERS_user_permissions_permission_id_f4415542" ON "USERS_user_permissions" ("permission_id");

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE INDEX "BREED_SCANS_user_id_6550d963" ON "BREED_SCANS" ("user_id");

CREATE INDEX "CHAT_HISTORY_session_id_62560f22" ON "CHAT_HISTORY" ("session_id");

CREATE INDEX "CHAT_HISTORY_user_id_d485cb12" ON "CHAT_HISTORY" ("user_id");

CREATE INDEX "WEIGHT_HISTORY_pet_id_5fc3f64b" ON "WEIGHT_HISTORY" ("pet_id");

CREATE INDEX "VACCINATIONS_pet_id_7cd8bac7" ON "VACCINATIONS" ("pet_id");

CREATE INDEX "MEDICINES_pet_id_4a976c5e" ON "MEDICINES" ("pet_id");

CREATE INDEX "HEALTH_RECORDS_pet_id_94cd0421" ON "HEALTH_RECORDS" ("pet_id");

CREATE INDEX "ALLERGIES_pet_id_36aa9bfb" ON "ALLERGIES" ("pet_id");

CREATE INDEX "LOST_PET_SIGHTINGS_lost_pet_id_ce8495a8" ON "LOST_PET_SIGHTINGS" ("lost_pet_id");

CREATE INDEX "MATCH_REQUESTS_receiver_profile_id_d2335471" ON "MATCH_REQUESTS" ("receiver_profile_id");

CREATE INDEX "MATCH_REQUESTS_sender_profile_id_e09f8618" ON "MATCH_REQUESTS" ("sender_profile_id");

CREATE INDEX "NOTIFICATIONS_user_id_1964353b" ON "NOTIFICATIONS" ("user_id");

CREATE INDEX "PETS_owner_id_6c79333d" ON "PETS" ("owner_id");

CREATE INDEX "RECOMMENDATIONS_pet_id_2561a301" ON "RECOMMENDATIONS" ("pet_id");

CREATE INDEX "RECOMMENDATIONS_user_id_ae0f6eef" ON "RECOMMENDATIONS" ("user_id");

CREATE INDEX "REVIEWS_caretaker_id_ed169357" ON "REVIEWS" ("caretaker_id");

CREATE INDEX "REVIEWS_reviewer_id_f273de1d" ON "REVIEWS" ("reviewer_id");

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

CREATE INDEX "LOST_PETS_reporter_id_e659e013" ON "LOST_PETS" ("reporter_id");

CREATE INDEX "PAYMENTS_razorpay_order_id_93802649" ON "PAYMENTS" ("razorpay_order_id");

CREATE INDEX "PAYMENTS_razorpay_payment_id_14516228" ON "PAYMENTS" ("razorpay_payment_id");

CREATE INDEX "ADOPTION_LISTINGS_owner_id_f5aa51ce" ON "ADOPTION_LISTINGS" ("owner_id");

CREATE INDEX "ADOPTION_LISTINGS_adopter_id_38e7a5ec" ON "ADOPTION_LISTINGS" ("adopter_id");

CREATE INDEX "ADOPTION_PAYMENTS_adopter_id_a4eb4b65" ON "ADOPTION_PAYMENTS" ("adopter_id");

CREATE INDEX "ADOPTION_PAYMENTS_listing_id_57a0a1b1" ON "ADOPTION_PAYMENTS" ("listing_id");

CREATE INDEX "ADOPTION_REQUESTS_applicant_id_92c94c05" ON "ADOPTION_REQUESTS" ("applicant_id");

CREATE INDEX "ADOPTION_REQUESTS_listing_id_d6576d05" ON "ADOPTION_REQUESTS" ("listing_id");

CREATE INDEX "BOOKINGS_caretaker_id_92ad6fc1" ON "BOOKINGS" ("caretaker_id");

CREATE INDEX "BOOKINGS_owner_id_beb37e0b" ON "BOOKINGS" ("owner_id");

CREATE INDEX "BOOKINGS_pet_id_fd663ad5" ON "BOOKINGS" ("pet_id");

CREATE UNIQUE INDEX "BOOKINGS_pets_booking_id_pet_id_2051da37_uniq" ON "BOOKINGS_pets" ("booking_id", "pet_id");

CREATE INDEX "BOOKINGS_pets_booking_id_7c4a7844" ON "BOOKINGS_pets" ("booking_id");

CREATE INDEX "BOOKINGS_pets_pet_id_0926a17d" ON "BOOKINGS_pets" ("pet_id");
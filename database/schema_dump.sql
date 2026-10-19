BEGIN TRANSACTION;
CREATE TABLE "ADOPTION_LISTINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "age" decimal NOT NULL, "gender" varchar(10) NOT NULL, "listing_type" varchar(20) NOT NULL, "price" decimal NOT NULL, "location" varchar(200) NOT NULL, "vaccination_status" varchar(50) NOT NULL, "description" text NOT NULL, "photo" varchar(100) NULL, "contact_phone" varchar(20) NOT NULL, "contact_email" varchar(254) NOT NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "adopter_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_status" varchar(20) NOT NULL);
INSERT INTO "ADOPTION_LISTINGS" VALUES(1,'Daisy','Dog','Beagle',0.8,'Female','ADOPTION',0,'Austin, TX','Fully Vaccinated & Microchipped','Daisy is a merry, sweet Beagle puppy looking for a loving home with a yard. Loves kids and get along with other dogs.','','+1 (555) 876-5432','david.miller@example.com','ACTIVE','2026-08-23 07:06:10.647668',3,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(2,'Simba','Cat','Maine Coon',1.2,'Male','ADOPTION',0,'Austin, TX','Up to date','Gentle giant Maine Coon! Very affectionate, purrs constantly, and enjoys company.','','+1 (555) 432-1098','priya.sharma@example.com','ACTIVE','2026-08-23 07:06:10.655128',4,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(3,'Daisy','Dog','Beagle',0.8,'Female','ADOPTION',0,'Indiranagar, Bengaluru','Fully Vaccinated & Microchipped','Daisy is a merry, sweet Beagle puppy looking for a loving home with a yard. Extremely friendly with children, crate trained, and loves outdoor walks.','listings/listing_001.jpg','+91 97312 34567','david.miller@example.com','ACTIVE','2026-10-15 22:57:40.578556',3,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(4,'Simba','Cat','Maine Coon',1.2,'Male','ADOPTION',0,'Bandra West, Mumbai','Up to date (Rabies + FVRCP)','Simba is a gentle giant Maine Coon with gorgeous fluffy fur! Loves curling up on laps, purrs loudly, and gets along well with calm dogs and cats.','listings/listing_002.jpg','+91 99001 23456','priya.sharma@example.com','ACTIVE','2026-10-15 22:57:40.584297',4,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(5,'Milo','Dog','Golden Retriever',2,'Male','ADOPTION',0,'Besant Nagar, Chennai','Fully Vaccinated & Neutered','Milo is a pure bundle of joy! He knows basic commands (sit, paw, stay), adores playing fetch in the park, and has an exceptionally gentle temperament.','listings/listing_003.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.591689',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(6,'Luna','Cat','Persian Cat',1.5,'Female','ADOPTION',0,'Koramangala, Bengaluru','Fully Vaccinated & Spayed','Luna is a placid, affectionate white Persian cat. She enjoys serene indoor living, daily soft grooming, and sitting beside sunny windows.','listings/listing_004.jpg','+91 98112 34567','sarah.jenkins@example.com','ACTIVE','2026-10-15 22:57:40.599278',2,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(7,'Rocky','Dog','German Shepherd',3,'Male','ADOPTION',0,'Jubilee Hills, Hyderabad','Complete Anti-Rabies & DHPP','Rocky is an intelligent, loyal German Shepherd. Highly alert, eager to please, and protective of family. Best suited for an active household.','listings/listing_005.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.606475',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(8,'Coco','Dog','Labrador Retriever',0.6,'Female','ADOPTION',0,'Vasant Kunj, New Delhi','Puppy Core Shots Completed','Coco is a playful chocolate Lab pup! Eager to learn, food-motivated, loves water games, and gets along fantastic with other pets.','listings/listing_006.jpg','+91 98765 11223','gopika@gmail.com','ACTIVE','2026-10-15 22:57:40.612072',50,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(9,'Leo','Dog','Indie / Desi Street Pup',0.4,'Male','ADOPTION',0,'Adyar, Chennai','First Vaccine Done & Dewormed','Rescued Indie pup with sharp intelligence and huge floppy ears. Extremely hardy, affectionate, fast learner, and looking for a loving home!','listings/listing_007.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.618797',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(10,'Bella','Dog','French Bulldog',2.5,'Female','ADOPTION',0,'Kothrud, Pune','Up to date with Health Records','Bella is a goofy Frenchie who loves couch cuddles and short evening walks. Low exercise needs, ideal apartment companion.','listings/listing_008.jpg','+91 98450 77889','aathi@gmail.com','ACTIVE','2026-10-15 22:57:40.626675',54,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(11,'Oliver','Cat','British Shorthair',1,'Male','ADOPTION',0,'Colaba, Mumbai','Vaccinated & Neutered','Plush grey coat with glowing amber eyes. Calm, independent, and tidy with litter box habits. Perfect for quiet apartment living.','listings/listing_009.jpg','+91 99001 23456','priya.sharma@example.com','ACTIVE','2026-10-15 22:57:40.633919',4,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(12,'Shadow','Dog','Siberian Husky',2.8,'Male','ADOPTION',0,'Whitefield, Bengaluru','Complete Annual Vaccines','Stunning bi-eyed Husky! High-energy boy who loves jogging, running in open fields, and communicating with adorable vocal howls.','listings/listing_010.jpg','+91 97312 34567','david.miller@example.com','ACTIVE','2026-10-15 22:57:40.641381',3,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(13,'Ruby','Cat','Indie Calico Kitten',0.3,'Female','ADOPTION',0,'T. Nagar, Chennai','Dewormed & First Tricat Shot','Cute tri-color calico rescue kitten! Playful, purrs on touch, loves chasing feather toys, and eats dry kibble and wet food eagerly.','listings/listing_011.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.646143',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(14,'Charlie','Dog','Shih Tzu',1.8,'Male','ADOPTION',0,'Salt Lake, Kolkata','Fully Vaccinated','Friendly lapdog with silky coat. Loves following owners room to room, great with children, and hypoallergenic.','listings/listing_012.jpg','+91 98112 34567','sarah.jenkins@example.com','ACTIVE','2026-10-15 22:57:40.652690',2,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(15,'Ginger','Cat','Siamese Cat',1.4,'Female','ADOPTION',0,'Gachibowli, Hyderabad','Up to date & Spayed','Striking sapphire blue eyes and pointed coat. Very vocal and interactive; greets you at the door every evening!','listings/listing_013.jpg','+91 98765 11223','gopika@gmail.com','ACTIVE','2026-10-15 22:57:40.660414',50,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(16,'Bruno','Dog','Rottweiler Puppy',0.5,'Male','SALE',2500,'Koramangala, Bengaluru','Core Puppy Vaccination Pack Complete','Certified champion bloodline pup with thick bone structure and calm temperament. Microchipped, vet checked, and leash started.','listings/listing_014.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.668501',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(17,'Cleo','Cat','Ragdoll',2.1,'Female','ADOPTION',0,'Saket, New Delhi','Fully Vaccinated & Dewormed','Goes limp with affection when held! Docile, gentle, and quiet. Needs an indoor-only home with loving companions.','listings/listing_015.jpg','+91 99001 23456','priya.sharma@example.com','ACTIVE','2026-10-15 22:57:40.675771',4,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(18,'Oreo','Dog','Border Collie',1.6,'Male','ADOPTION',0,'Andheri West, Mumbai','Complete Vaccinations','Super smart working dog! Knows 15+ tricks, agility ready, loves frisbee, and thrives on mental stimulation and training.','listings/listing_016.jpg','+91 97312 34567','david.miller@example.com','ACTIVE','2026-10-15 22:57:40.682507',3,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(19,'Maya','Dog','Indie Rescue Pup',0.5,'Female','ADOPTION',0,'Anna Nagar, Chennai','Vaccinated & Dewormed','Sweet golden Indie female pup rescued from highway. Extremely loving, resilient, and ready for a compassionate family to adopt her.','listings/listing_017.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.690081',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(20,'Casper','Cat','Bengal Cat',1.1,'Male','ADOPTION',0,'Viman Nagar, Pune','Up to date with Rabies & Tricat','Gorgeous leopard rosette coat! Active, curious, loves climbing tall cat trees and watching birds.','listings/listing_018.jpg','+91 98450 77889','aathi@gmail.com','ADOPTED','2026-10-15 22:57:40.697617',54,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(21,'Puggy','Dog','Pug',3.2,'Female','ADOPTION',0,'HSR Layout, Bengaluru','Fully Vaccinated','Charming fawn pug with a curly tail! Loves afternoon naps, snuggling on the sofa, and making adorable snorting sounds.','listings/listing_019.jpg','+91 98112 34567','sarah.jenkins@example.com','ACTIVE','2026-10-15 22:57:40.704956',2,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(22,'Snowball','Rabbit','Holland Lop',0.9,'Female','ADOPTION',0,'Mylapore, Chennai','Health Checked & Vaccinated (RHDV)','Fluffy white lop-eared bunny! Litter-box trained, eats hay and leafy greens happily, and enjoys gentle petting.','listings/listing_020.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.712533',55,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(23,'Maximus','Dog','Cocker Spaniel',2.2,'Male','ADOPTION',0,'Banjara Hills, Hyderabad','Full Annual Boosters Complete','Golden Cocker Spaniel with soulful brown eyes and soft silky ears. Very affectionate, wonderful with children, and loves park strolls.','listings/listing_021.jpg','+91 98765 11223','gopika@gmail.com','ACTIVE','2026-10-15 22:57:40.720753',50,NULL,'UNPAID');
INSERT INTO "ADOPTION_LISTINGS" VALUES(24,'Nala','Cat','Tabby Kitten',0.3,'Female','ADOPTION',0,'Powai, Mumbai','First Shot & Deworming Completed','Energetic brown striped tabby kitten! Loves sprinting after bouncy balls, purring like a motor, and falling asleep on your lap.','listings/listing_022.jpg','+91 98401 22334','adoptions@pawsindia.org','ACTIVE','2026-10-15 22:57:40.727895',55,NULL,'UNPAID');
CREATE TABLE "ADOPTION_PAYMENTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "razorpay_order_id" varchar(100) NOT NULL UNIQUE, "razorpay_payment_id" varchar(100) NULL, "razorpay_signature" varchar(255) NULL, "amount" decimal NOT NULL, "currency" varchar(10) NOT NULL, "status" varchar(20) NOT NULL, "payment_method" varchar(60) NOT NULL, "error_code" varchar(100) NULL, "error_description" text NULL, "paid_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "adopter_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "listing_id" bigint NOT NULL REFERENCES "ADOPTION_LISTINGS" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "ADOPTION_REQUESTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "applicant_name" varchar(120) NOT NULL, "applicant_email" varchar(254) NOT NULL, "applicant_phone" varchar(30) NOT NULL, "housing_type" varchar(100) NOT NULL, "pet_experience" varchar(100) NOT NULL, "message" text NOT NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "applicant_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "listing_id" bigint NOT NULL REFERENCES "ADOPTION_LISTINGS" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "ALLERGIES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "allergy_name" varchar(150) NOT NULL, "severity" varchar(20) NOT NULL, "notes" text NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "ALLERGIES" VALUES(1,'Dust sensitivity','Moderate','Prevent exposure to Dust sensitivity. Administer antihistamine under vet guidance if reaction occurs.','2026-09-14 13:40:07.717791',6);
INSERT INTO "ALLERGIES" VALUES(2,'Chicken allergy','Moderate','Prevent exposure to Chicken allergy. Administer antihistamine under vet guidance if reaction occurs.','2026-09-14 13:40:07.747917',10);
INSERT INTO "ALLERGIES" VALUES(3,'Ear sensitivity','Moderate','Prevent exposure to Ear sensitivity. Administer antihistamine under vet guidance if reaction occurs.','2026-09-14 13:40:07.827719',24);
INSERT INTO "ALLERGIES" VALUES(4,'Cold sensitivity','Moderate','Prevent exposure to Cold sensitivity. Administer antihistamine under vet guidance if reaction occurs.','2026-09-14 13:40:07.895835',36);
CREATE TABLE "BOOKINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "service_type" varchar(100) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "start_time" varchar(10) NOT NULL, "end_time" varchar(10) NOT NULL, "total_price" decimal NOT NULL, "notes" text NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "caretaker_id" bigint NOT NULL REFERENCES "CARETAKERS" ("id") DEFERRABLE INITIALLY DEFERRED, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_status" varchar(20) NOT NULL, "arrival_time" varchar(20) NULL, "emergency_fee" decimal NOT NULL, "emergency_phone" varchar(20) NULL, "emergency_reason" text NULL, "is_emergency" bool NOT NULL);
INSERT INTO "BOOKINGS" VALUES(1,'Pet Sitting','2026-08-09','2026-08-11','09:00 AM','06:00 PM',336,'Max was super excited and well taken care of!','COMPLETED','2026-08-23 07:06:10.603106','2026-08-23 07:06:10.603106',1,2,1,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(2,'Overnight Boarding','2026-08-28','2026-08-31','10:00 AM','04:00 PM',420,'Luna needs her probiotic powder daily.','ACCEPTED','2026-08-23 07:06:10.625824','2026-10-15 22:46:47.623123',2,2,2,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(3,'Dog Walking','2026-08-25','2026-08-26','08:00 AM','12:00 PM',168,'Need morning agility walk around Zilker Park.','PENDING','2026-08-23 07:06:10.635284','2026-08-23 07:06:10.635284',1,3,3,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(4,'Pet Sitting','2026-08-20','2026-08-22','09:00 AM','05:00 PM',1500,'Demo booking for Bruno with Priya.','COMPLETED','2026-09-14 13:40:07.550189','2026-09-14 13:41:01.528992',5,10,5,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(5,'Daycare','2026-08-27','2026-08-28','09:00 AM','05:00 PM',1000,'Demo booking for Luna with Priya.','COMPLETED','2026-09-14 13:40:07.552942','2026-09-14 13:41:01.530744',5,10,6,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(6,'Dog Walking','2026-09-02','2026-09-02','09:00 AM','05:00 PM',500,'Demo booking for Rocky with Priya.','COMPLETED','2026-09-14 13:40:07.554594','2026-09-14 13:41:01.531821',5,11,8,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(7,'Overnight Boarding','2026-08-15','2026-08-18','09:00 AM','05:00 PM',2600,'Demo booking for Simba with Suresh.','COMPLETED','2026-09-14 13:40:07.557073','2026-09-14 13:41:01.533250',6,12,10,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(8,'Grooming & Bath','2026-08-23','2026-08-23','09:00 AM','05:00 PM',650,'Demo booking for Charlie with Suresh.','COMPLETED','2026-09-14 13:40:07.558667','2026-09-14 13:41:01.533870',6,13,13,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(9,'Dog Walking','2026-08-30','2026-08-31','09:00 AM','05:00 PM',900,'Demo booking for Shadow with Karthikeyan.','COMPLETED','2026-09-14 13:40:07.560309','2026-09-14 13:41:01.535111',7,14,15,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(10,'Pet Sitting','2026-08-17','2026-08-19','09:00 AM','05:00 PM',1650,'Demo booking for Daisy with Deepa.','COMPLETED','2026-09-14 13:40:07.560309','2026-09-14 13:41:01.536349',8,15,18,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(11,'Dog Walking','2026-08-25','2026-08-25','09:00 AM','05:00 PM',400,'Demo booking for Tyson with Ramesh.','COMPLETED','2026-09-14 13:40:07.560309','2026-09-14 13:41:01.537707',9,16,20,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(12,'Pet Sitting','2026-08-31','2026-09-01','09:00 AM','05:00 PM',1400,'Demo booking for Ginger with Preethi.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.538949',10,17,22,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(13,'Dog Walking','2026-08-19','2026-08-21','09:00 AM','05:00 PM',1050,'Demo booking for Cooper with Manikandan.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.539567',11,18,24,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(14,'Daycare','2026-09-04','2026-09-05','09:00 AM','05:00 PM',960,'Demo booking for Leo with Gowri.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.539567',12,19,27,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(15,'Overnight Boarding','2026-08-13','2026-08-17','09:00 AM','05:00 PM',3750,'Demo booking for Buster with Revathi.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.539567',13,20,29,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(16,'Dog Walking','2026-08-29','2026-08-30','09:00 AM','05:00 PM',760,'Demo booking for Casper with Ashok.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.539567',14,21,31,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(17,'Pet Sitting','2026-08-24','2026-08-26','09:00 AM','05:00 PM',1560,'Demo booking for Thor with Bhuvaneshwari.','COMPLETED','2026-09-14 13:40:07.565311','2026-09-14 13:41:01.544684',15,22,33,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(18,'Overnight Boarding','2026-08-26','2026-08-27','09:00 AM','05:00 PM',1200,'Demo booking for Zoe with Vignesh.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.544684',16,23,36,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(19,'Pet Sitting','2026-08-21','2026-08-22','09:00 AM','05:00 PM',600,'Demo booking for Bruno Jr with Jayanthi.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.544684',17,24,38,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(20,'Dog Walking','2026-09-03','2026-09-03','09:00 AM','05:00 PM',540,'Demo booking for Simba Cat with Anandhi.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.544684',18,25,40,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(21,'Dog Walking','2026-08-16','2026-08-17','09:00 AM','05:00 PM',840,'Demo booking for Maximus with Dinesh.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.544684',19,26,42,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(22,'Grooming & Bath','2026-08-28','2026-08-28','09:00 AM','05:00 PM',680,'Demo booking for Maya with Geetha.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.544684',20,27,45,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(23,'Dog Walking','2026-09-01','2026-09-02','09:00 AM','05:00 PM',560,'Demo booking for Rex with Naveen.','COMPLETED','2026-09-14 13:40:07.573561','2026-09-14 13:41:01.553055',21,28,47,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(24,'Overnight Boarding','2026-08-18','2026-08-21','09:00 AM','05:00 PM',2320,'Demo booking for Teddy with Lakshmi.','COMPLETED','2026-09-14 13:40:07.582190','2026-09-14 13:41:01.553055',22,29,49,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(25,'Dog Walking','2026-09-06','2026-09-06','09:00 AM','05:00 PM',800,'Demo booking for Bruno with Hariprasad.','COMPLETED','2026-09-14 13:40:07.582190','2026-09-14 13:41:01.555064',23,10,5,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(26,'Pet Sitting','2026-09-05','2026-09-06','09:00 AM','05:00 PM',920,'Demo booking for Milo with Shalini.','COMPLETED','2026-09-14 13:40:07.582190','2026-09-14 13:41:01.557075',24,11,9,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(27,'Dog Walking','2026-09-08','2026-09-08','09:00 AM','05:00 PM',500,'Demo booking for Bella with Priya.','COMPLETED','2026-09-14 13:40:07.582190','2026-09-14 13:41:01.557075',5,12,11,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(28,'Pet Sitting','2026-09-07','2026-09-08','09:00 AM','05:00 PM',1300,'Demo booking for Oliver with Suresh.','COMPLETED','2026-09-14 13:40:07.582190','2026-09-14 13:41:01.559082',6,13,14,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(29,'Dog Walking','2026-09-17','2026-09-18','09:00 AM','05:00 PM',1000,'Demo booking for Bruno with Priya.','ACCEPTED','2026-09-14 13:40:07.582190','2026-10-18 08:24:24.559179',5,10,5,'PAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(30,'Overnight Boarding','2026-09-19','2026-09-21','09:00 AM','05:00 PM',1950,'Demo booking for Rocky with Suresh.','ACCEPTED','2026-09-14 13:40:07.588216','2026-09-14 13:41:01.561089',6,11,8,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(31,'Daycare','2026-09-16','2026-09-16','09:00 AM','05:00 PM',450,'Demo booking for Simba with Karthikeyan.','ACCEPTED','2026-09-14 13:40:07.589966','2026-09-14 13:41:01.561089',7,12,10,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(32,'Pet Sitting','2026-09-18','2026-09-19','09:00 AM','05:00 PM',1100,'Demo booking for Lily with Deepa.','ACCEPTED','2026-09-14 13:40:07.589966','2026-09-14 13:41:01.561089',8,14,16,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(33,'Grooming & Bath','2026-09-20','2026-09-20','09:00 AM','05:00 PM',700,'Demo booking for Daisy with Preethi.','ACCEPTED','2026-09-14 13:40:07.589966','2026-09-14 13:41:01.561089',10,15,18,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(34,'Daycare','2026-09-17','2026-09-18','09:00 AM','05:00 PM',960,'Demo booking for Ginger with Gowri.','ACCEPTED','2026-09-14 13:40:07.589966','2026-09-14 13:41:01.561089',12,17,22,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(35,'Pet Sitting','2026-09-19','2026-09-21','09:00 AM','05:00 PM',2250,'Demo booking for Cooper with Revathi.','ACCEPTED','2026-09-14 13:40:07.595787','2026-09-14 13:41:01.561089',13,18,24,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(36,'Dog Walking','2026-09-21','2026-09-22','09:00 AM','05:00 PM',760,'Demo booking for Leo with Ashok.','PENDING','2026-09-14 13:40:07.595787','2026-09-14 13:41:01.561089',14,19,27,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(37,'Pet Sitting','2026-09-22','2026-09-24','09:00 AM','05:00 PM',1560,'Demo booking for Buster with Bhuvaneshwari.','PENDING','2026-09-14 13:40:07.598399','2026-09-14 13:41:01.561089',15,20,29,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(38,'Pet Sitting','2026-09-24','2026-09-25','09:00 AM','05:00 PM',600,'Demo booking for Thor with Jayanthi.','PENDING','2026-09-14 13:40:07.598399','2026-09-14 13:41:01.569670',17,22,33,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(39,'Dog Walking','2026-09-23','2026-09-23','09:00 AM','05:00 PM',420,'Demo booking for Bruno Jr with Dinesh.','PENDING','2026-09-14 13:40:07.598399','2026-09-14 13:41:01.569670',19,24,38,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(40,'Dog Walking','2026-09-25','2026-09-26','09:00 AM','05:00 PM',560,'Demo booking for Maximus with Naveen.','PENDING','2026-09-14 13:40:07.598399','2026-09-14 13:41:01.569670',21,26,42,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(41,'Overnight Boarding','2026-09-09','2026-09-10','09:00 AM','05:00 PM',1160,'Demo booking for Maya with Lakshmi.','CANCELLED','2026-09-14 13:40:07.607386','2026-09-14 13:41:01.569670',22,27,45,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(42,'Dog Walking','2026-09-10','2026-09-10','09:00 AM','05:00 PM',800,'Demo booking for Rex with Hariprasad.','CANCELLED','2026-09-14 13:40:07.607386','2026-09-14 13:41:01.569670',23,28,47,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(43,'Pet Sitting','2026-09-11','2026-09-12','09:00 AM','05:00 PM',920,'Demo booking for Teddy with Shalini.','REJECTED','2026-09-14 13:40:07.607386','2026-09-14 13:41:01.569670',24,29,49,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(44,'Pet Sitting','2026-10-20','2026-10-20','09:00 AM','05:00 PM',2160,'','ACCEPTED','2026-10-17 18:17:31.563250','2026-10-18 11:08:58.221342',18,10,7,'UNPAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(45,'Overnight Boarding','2026-10-20','2026-10-21','09:00 AM','05:00 PM',4320,'','ACCEPTED','2026-10-18 05:53:01.539925','2026-10-18 06:40:56.467818',18,10,7,'PAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(46,'Daycare','2026-10-28','2026-10-28','09:00 AM','05:00 PM',1800,'','ACCEPTED','2026-10-18 08:34:13.354107','2026-10-18 10:42:37.150458',7,10,6,'PAID',NULL,0,NULL,NULL,0);
INSERT INTO "BOOKINGS" VALUES(47,'Pet Sitting','2026-10-25','2026-10-25','09:00 AM','05:00 PM',0,NULL,'ACCEPTED','2026-10-18 11:28:02.893678','2026-10-18 11:28:02.893678',2,10,7,'UNPAID',NULL,0,NULL,NULL,0);
CREATE TABLE "BOOKINGS_pets" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking_id" bigint NOT NULL REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "BREED_SCANS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "predicted_breed" varchar(100) NOT NULL, "confidence_score" decimal NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "BREED_SCANS" VALUES(1,'scans/shutterstock_2531111131_crop-ed-A-black-Affenpinscher-sits-proudly-showcasing-its_4oQXJzA.webp','Persian Cat',78.5,'2026-08-23 08:28:12.575560',2);
INSERT INTO "BREED_SCANS" VALUES(2,'scans/shutterstock_2531111131_crop-ed-A-black-Affenpinscher-sits-proudly-showcasing-its_DgDK55E.webp','Scottish Terrier',82,'2026-08-23 08:55:37.223545',2);
INSERT INTO "BREED_SCANS" VALUES(3,'scans/shutterstock_2531111131_crop-ed-A-black-Affenpinscher-sits-proudly-showcasing-its_DYbSEdc.webp','Affenpinscher',96.5,'2026-08-23 09:16:26.218014',2);
INSERT INTO "BREED_SCANS" VALUES(4,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog.avif','Labrador Retriever',82,'2026-08-23 09:16:38.765128',2);
INSERT INTO "BREED_SCANS" VALUES(5,'scans/360_F_315768136_eajPfAay13gLRvAYN4KRQ0NjpciJyaeS.jpg','Affenpinscher',96.5,'2026-08-23 09:20:13.535654',2);
INSERT INTO "BREED_SCANS" VALUES(6,'scans/360_F_315768136_eajPfAay13gLRvAYN4KRQ0NjpciJyaeS_hEMt24b.jpg','Ibizan Hound',76.5,'2026-08-23 09:29:27.035856',2);
INSERT INTO "BREED_SCANS" VALUES(7,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog_mscX9VN.avif','King Charles Spaniel',98.6,'2026-08-23 09:29:44.463460',2);
INSERT INTO "BREED_SCANS" VALUES(8,'scans/shutterstock_2531111131_crop-ed-A-black-Affenpinscher-sits-proudly-showcasing-its_j7shaRx.webp','Affenpinscher',99.2,'2026-08-23 10:02:51.183696',2);
INSERT INTO "BREED_SCANS" VALUES(9,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog_PG3pxzy.avif','King Charles Spaniel',98.6,'2026-08-23 10:03:03.129376',2);
INSERT INTO "BREED_SCANS" VALUES(10,'scans/Abyssinian-Cat-Breed_0.webp','Egyptian Mau Cat',81.3,'2026-08-23 10:06:00.258957',2);
INSERT INTO "BREED_SCANS" VALUES(11,'scans/Abyssinian-Cat-Breed_0_skixOSf.webp','Egyptian Mau Cat',81.3,'2026-08-23 10:29:12.191091',2);
INSERT INTO "BREED_SCANS" VALUES(12,'scans/Abyssinian-Cat-Breed_0_XqkEPSm.webp','Egyptian Mau Cat',79.6,'2026-08-23 10:54:43.731846',2);
INSERT INTO "BREED_SCANS" VALUES(13,'scans/Abyssinian-Cat-Breed_0_l7dP9mW.webp','Egyptian Mau Cat',79.6,'2026-08-23 10:54:55.964540',2);
INSERT INTO "BREED_SCANS" VALUES(14,'scans/Abyssinian-Cat-Breed_0_prSuAqP.webp','Egyptian Mau Cat',79.6,'2026-08-23 10:55:52.212318',2);
INSERT INTO "BREED_SCANS" VALUES(15,'scans/Abyssinian-Cat-Breed_0_4HYvADR.webp','Egyptian Mau Cat',90.6,'2026-08-23 11:02:16.921672',2);
INSERT INTO "BREED_SCANS" VALUES(16,'scans/shutterstock_2531111131_crop-ed-A-black-Affenpinscher-sits-proudly-showcasing-its_el15xLs.webp','Affenpinscher',99.3,'2026-08-23 11:02:28.956948',2);
INSERT INTO "BREED_SCANS" VALUES(17,'scans/Abyssinian-Cat-Breed_0_snsMThb.webp','Siamese Cat',82,'2026-08-23 11:10:31.902227',2);
INSERT INTO "BREED_SCANS" VALUES(18,'scans/Abyssinian-Cat-Breed_0_g8OdiH3.webp','Abyssinian Cat',86.5,'2026-08-23 11:21:10.355289',2);
INSERT INTO "BREED_SCANS" VALUES(19,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog_yDSGWs2.avif','King Charles Spaniel',93.4,'2026-08-23 11:21:51.194435',2);
INSERT INTO "BREED_SCANS" VALUES(20,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog_V0LyDjK.avif','King Charles Spaniel',93.4,'2026-08-23 11:27:48.455414',2);
INSERT INTO "BREED_SCANS" VALUES(21,'scans/pug-dog-isolated-white-background_2829-11416.avif','Pug',97.6,'2026-08-23 11:29:12.516578',2);
INSERT INTO "BREED_SCANS" VALUES(22,'scans/beagle-hound-dog.webp','English Foxhound',78.5,'2026-08-23 11:30:31.928745',2);
INSERT INTO "BREED_SCANS" VALUES(23,'scans/beagle-hound-dog_5OF9aBF.webp','Beagle',99.4,'2026-08-23 11:41:21.549309',2);
INSERT INTO "BREED_SCANS" VALUES(24,'scans/adorable-cavalier-king-charles-spaniel-puppy-royalty-dog_BBmexfr.avif','King Charles Spaniel',92.9,'2026-08-23 11:48:33.560573',2);
INSERT INTO "BREED_SCANS" VALUES(25,'scans/pug-dog-isolated-white-background_2829-11416_W2oxyAW.avif','Pug',97.6,'2026-09-14 13:03:33.884022',9);
INSERT INTO "BREED_SCANS" VALUES(26,'scans/beagle-hound-dog_EzfSyqO.webp','Beagle',99.4,'2026-09-14 13:03:48.676681',9);
INSERT INTO "BREED_SCANS" VALUES(27,'scans/pug-dog-isolated-white-background_2829-11416_CCVFX0F.avif','Pug',97.6,'2026-10-01 20:06:45.334864',10);
CREATE TABLE "CARETAKERS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "experience_years" decimal NOT NULL, "hourly_rate" decimal NOT NULL, "services_offered" varchar(500) NOT NULL, "availability_status" varchar(20) NOT NULL, "bio" text NULL, "rating" decimal NOT NULL, "total_reviews" integer unsigned NOT NULL CHECK ("total_reviews" >= 0), "total_earnings" decimal NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "CARETAKERS" VALUES(1,4.5,28,'Pet Sitting, Dog Walking, Agility Play, Daycare','AVAILABLE','Certified veterinary technician assistant with 4+ years of hands-on pet sitting experience. Passionate about keeping energetic dogs active and giving cats peaceful attention.',5,1,1580,'2026-08-23 07:06:08.617213','2026-08-23 07:06:08.617213',5);
INSERT INTO "CARETAKERS" VALUES(2,6,35,'Senior Pet Care, Overnight Boarding, Medication Administration, Grooming','AVAILABLE','Specialized senior pet and post-surgery care provider. Experienced in administering oral and subcutaneous medications with extreme gentleness and precision.',5,42,2840,'2026-08-23 07:06:09.154499','2026-08-23 07:06:09.154499',6);
INSERT INTO "CARETAKERS" VALUES(3,3,24,'High-Energy Dog Walking, Puppy Training, Adventure Hikes','AVAILABLE','Canine fitness enthusiast who loves trail running and agility training with active large breeds like Huskies, Shepherds, and Labradors.',4.85,19,1120,'2026-08-23 07:06:09.664121','2026-08-23 07:06:09.664121',7);
INSERT INTO "CARETAKERS" VALUES(4,2.5,22,'Cat Sitting, Gentle In-Home Sitting, Grooming & Bath','BUSY','Feline behavior specialist. Expert in shy and nervous cats, administering brush-outs, and gentle cuddles in a stress-free home environment.',4.9,16,860,'2026-08-23 07:06:10.166837','2026-08-23 07:06:10.166837',8);
INSERT INTO "CARETAKERS" VALUES(5,5.5,500,'Pet Sitting, Dog Walking, Feeding, Daycare','AVAILABLE','Certified canine behaviorist & pet nutritionist with 5+ years of dedicated pet care experience across Madurai.',4.75,4,3500,'2026-09-14 13:40:00.995763','2026-09-14 13:40:55.636658',30);
INSERT INTO "CARETAKERS" VALUES(6,7,650,'Pet Sitting, Dog Walking, Overnight Boarding, Grooming & Bath','AVAILABLE','Former veterinary technician offering specialized senior pet nursing, post-surgery care, and calm overnight boarding.',4.33,3,0,'2026-09-14 13:40:01.328816','2026-09-14 13:40:55.949747',31);
INSERT INTO "CARETAKERS" VALUES(7,4,450,'Dog Walking, Daycare, Pet Sitting','AVAILABLE','Energetic dog fitness coach and trail runner. Your furry friend will enjoy long, stimulating outdoor exercise sessions.',5,1,900,'2026-09-14 13:40:01.643692','2026-09-14 13:40:56.238798',32);
INSERT INTO "CARETAKERS" VALUES(8,6.2,550,'Pet Sitting, Feeding, Daycare, Grooming & Bath','AVAILABLE','Cat whisperer and small animal specialist. Calm, quiet home environment with multiple climbing trees and safe indoor zones.',5,1,0,'2026-09-14 13:40:01.939048','2026-09-14 13:40:56.583001',33);
INSERT INTO "CARETAKERS" VALUES(9,3.5,400,'Dog Walking, Feeding, Pet Sitting','AVAILABLE','Punctual, friendly caretaker providing daily home check-ins, hydration monitoring, and medication administration.',4,1,0,'2026-09-14 13:40:02.238197','2026-09-14 13:40:56.865924',34);
INSERT INTO "CARETAKERS" VALUES(10,8,700,'Pet Sitting, Overnight Boarding, Grooming & Bath','AVAILABLE','Professional pet groomer and fear-free certified handler. Spacious climate-controlled boarding facility.',5,1,0,'2026-09-14 13:40:02.492235','2026-09-14 13:40:57.178805',35);
INSERT INTO "CARETAKERS" VALUES(11,2.5,350,'Dog Walking, Pet Sitting, Feeding','AVAILABLE','Dedicated animal lover providing structured walks, engaging playtime, and loving attention to domestic pets.',4,1,0,'2026-09-14 13:40:02.882733','2026-09-14 13:40:57.470063',36);
INSERT INTO "CARETAKERS" VALUES(12,5,480,'Pet Sitting, Dog Walking, Daycare','AVAILABLE','Experienced in caring for large working breeds with tailored exercise and agility routines.',5,1,0,'2026-09-14 13:40:03.265605','2026-09-14 13:40:57.755961',37);
INSERT INTO "CARETAKERS" VALUES(13,9.5,750,'Pet Sitting, Overnight Boarding, Grooming & Bath, Feeding','AVAILABLE','Senior pet nurse with nearly a decade of experience in dietary planning, emergency care, and loving boarding.',5,1,0,'2026-09-14 13:40:03.570669','2026-09-14 13:40:58.133678',38);
INSERT INTO "CARETAKERS" VALUES(14,3,380,'Dog Walking, Feeding, Daycare','AVAILABLE','Weekend sitter and energetic companion for dogs that love play sessions, ball fetch, and interactive brain puzzles.',4,1,0,'2026-09-14 13:40:03.890240','2026-09-14 13:40:58.456633',39);
INSERT INTO "CARETAKERS" VALUES(15,4.5,520,'Pet Sitting, Daycare, Grooming & Bath','AVAILABLE','Gentle handler for anxious and rescue pets. Focuses on positive reinforcement and stress-free socialization.',5,1,0,'2026-09-14 13:40:04.199897','2026-09-14 13:40:58.810684',40);
INSERT INTO "CARETAKERS" VALUES(16,6,600,'Overnight Boarding, Daycare, Pet Sitting','AVAILABLE','Secure home boarding with 24/7 camera monitoring, private grassy play yard, and constant companionship.',4,1,0,'2026-09-14 13:40:04.481276','2026-09-14 13:40:59.057851',41);
INSERT INTO "CARETAKERS" VALUES(17,2,300,'Pet Sitting, Feeding, Dog Walking','AVAILABLE','Loving family environment for small dogs, puppies, and bunnies. Safe indoor playtime and constant affection.',5,1,0,'2026-09-14 13:40:04.794867','2026-09-14 13:40:59.372966',42);
INSERT INTO "CARETAKERS" VALUES(18,5.8,540,'Dog Walking, Pet Sitting, Overnight Boarding','AVAILABLE','Certified pet CPR and first responder. Real-time GPS walking routes and photo updates sent during every session.',5,1,2700,'2026-09-14 13:40:05.108294','2026-09-14 13:40:59.687424',43);
INSERT INTO "CARETAKERS" VALUES(19,3.8,420,'Dog Walking, Daycare, Feeding','AVAILABLE','Passionate walker who ensures your pets receive both physical exercise and mental stimulation.',4,1,0,'2026-09-14 13:40:05.462961','2026-09-14 13:41:00.052620',44);
INSERT INTO "CARETAKERS" VALUES(20,7.5,680,'Pet Sitting, Grooming & Bath, Overnight Boarding','AVAILABLE','Holistic pet care practitioner offering organic home-cooked meals, gentle herbal bathing, and attentive care.',5,1,0,'2026-09-14 13:40:05.752477','2026-09-14 13:41:00.325072',45);
INSERT INTO "CARETAKERS" VALUES(21,1.8,280,'Dog Walking, Feeding','BUSY','Punctual, attentive morning walker with a focus on leash safety and hydration.',4,1,0,'2026-09-14 13:40:05.985034','2026-09-14 13:41:00.601727',46);
INSERT INTO "CARETAKERS" VALUES(22,6.5,580,'Overnight Boarding, Daycare, Dog Walking','AVAILABLE','Spacious countryside property with lush fenced run areas, natural swimming splash ponds, and agility ramps.',5,1,0,'2026-09-14 13:40:06.324096','2026-09-14 13:41:00.887483',47);
INSERT INTO "CARETAKERS" VALUES(23,10,800,'Pet Sitting, Dog Walking, Overnight Boarding, Daycare','AVAILABLE','Master canine handler and trainer with 10 years in obedience instruction, agility, and premium boarding.',5,1,0,'2026-09-14 13:40:06.613977','2026-09-14 13:41:01.160568',48);
INSERT INTO "CARETAKERS" VALUES(24,4.2,460,'Pet Sitting, Feeding, Grooming & Bath','AVAILABLE','Compassionate neighborhood pet sitter offering overnight home stays and personalized grooming sessions.',4,1,0,'2026-09-14 13:40:06.913809','2026-09-14 13:41:01.487976',49);
CREATE TABLE "CHAT_HISTORY" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "session_id" varchar(100) NOT NULL, "user_query" text NOT NULL, "bot_response" text NOT NULL, "model_used" varchar(50) NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "CHAT_HISTORY" VALUES(1,'guest','What foods are healthy for a Labrador?','🐶 **Labrador Retrievers** are friendly, energetic, and eager to please! They need **60-90 minutes of daily exercise** and love retrieving games and swimming. Prone to overeating, so monitor portions closely to prevent obesity. Feed high-quality large-breed kibble rich in glucosamine for joint health.','domain_expert_fallback','2026-08-23 07:57:35.119471',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(2,'guest','What foods are healthy for a Labrador?','🐶 **Labrador Retrievers** are friendly, energetic, and eager to please! They need **60-90 minutes of daily exercise** and love retrieving games and swimming. Prone to overeating, so monitor portions closely to prevent obesity. Feed high-quality large-breed kibble rich in glucosamine for joint health.','domain_expert_fallback','2026-08-23 07:58:16.782996',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(3,'f206932e-3cb0-4776-89e8-408b673005ee','hi','🐾 Hello! I am your **Pet Care Companion AI Assistant**. I can help you with personalized feeding advice, breed guides, grooming tips, vaccination schedules, puppy/kitten training, and daily pet care routines. How can I assist you and your furry friend today?','domain_expert_fallback','2026-08-23 08:24:21.726153',2);
INSERT INTO "CHAT_HISTORY" VALUES(4,'f206932e-3cb0-4776-89e8-408b673005ee','What vaccinations does a puppy need?','💉 **Essential Pet Vaccination Schedule:**
- **Puppies (6, 10, 14 weeks):** DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza), Rabies at 12-16 weeks, Bordetella (Kennel Cough).
- **Kittens (8, 12, 16 weeks):** FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia) and Rabies.
- **Adult Boosters:** Rabies (every 1-3 years) and Core boosters annually or triennially.
- **Deworming:** Routine preventive deworming every 3-6 months based on vet recommendation.','domain_expert_fallback','2026-08-23 08:24:51.202261',2);
INSERT INTO "CHAT_HISTORY" VALUES(5,'f206932e-3cb0-4776-89e8-408b673005ee','What vaccinations does a puppy need?','💉 **Essential Pet Vaccination Schedule:**
- **Puppies (6, 10, 14 weeks):** DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza), Rabies at 12-16 weeks, Bordetella (Kennel Cough).
- **Kittens (8, 12, 16 weeks):** FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia) and Rabies.
- **Adult Boosters:** Rabies (every 1-3 years) and Core boosters annually or triennially.
- **Deworming:** Routine preventive deworming every 3-6 months based on vet recommendation.','domain_expert_fallback','2026-08-23 08:25:10.263829',2);
INSERT INTO "CHAT_HISTORY" VALUES(6,'f206932e-3cb0-4776-89e8-408b673005ee','how to feed my puppy luna','🥣 **Optimal Pet Nutrition Guidelines:**
- **Puppies/Kittens:** Require high-protein (28%+), DHA-enriched diets for skeletal and brain development. Feed 3-4 portioned meals daily.
- **Adults:** Complete balanced diet matching activity level. Feed 2 meals daily.
- **Seniors:** Lower calorie, higher fiber, supplemented with Omega-3 fatty acids and Glucosamine for joint mobility.
- Always ensure fresh, clean water is accessible 24/7.','domain_expert_fallback','2026-08-23 08:25:50.186312',2);
INSERT INTO "CHAT_HISTORY" VALUES(7,'guest','how to feed my puppy luna','🥣 **Tailored Puppy Feeding Guide for your puppy **Luna**:**

Puppies grow at a rapid rate and require balanced calories, high-grade protein (**28%+**), calcium, phosphorus, and **DHA** for healthy skeletal and brain development.

### 📅 Recommended Daily Feeding Schedule:
1. **6 to 12 Weeks (Weaning Stage):** 
   - Feed **4 small meals daily** spaced evenly (e.g., 7:00 AM, 11:30 AM, 4:00 PM, 8:00 PM).
   - Soften premium puppy kibble with warm water or puppy milk replacer into a moist porridge.
2. **3 to 6 Months (Rapid Growth):** 
   - Reduce to **3 meals daily**.
   - Feed crunchy dry puppy kibble to promote jaw exercise and soothe teething gums.
3. **6 to 12 Months (Adolescence):** 
   - Transition to **2 meals daily** (morning & evening).
4. **12 Months (Adult Transition):** 
   - Gradually mix adult dog food over 7 days (25% -> 50% -> 75% -> 100%) to prevent digestive upset.

### ⚖️ Daily Portion & Practical Tips:
- **Measure by Weight:** Check the manufacturer feeding chart on your puppy kibble bag based on target adult weight. Split the total daily amount equally across meal times.
- **Hydration:** Keep fresh, clean water available in a shallow, tip-proof bowl 24/7.
- **Avoid Table Scraps:** Human seasonings, onions, garlic, and fatty trimmings cause severe gastrointestinal distress and pancreatitis.
- **Healthy Puppy Treats:** Use small pieces of boiled chicken breast, carrot coins, or single-ingredient training treats for positive reinforcement.','domain_expert_engine','2026-08-23 08:32:08.163820',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(8,'guest','how to feed my puppy luna','🥣 **Tailored Puppy Feeding Guide for your puppy **Luna**:**

Puppies grow at a rapid rate and require balanced calories, high-grade protein (**28%+**), calcium, phosphorus, and **DHA** for healthy skeletal and brain development.

### 📅 Recommended Daily Feeding Schedule:
1. **6 to 12 Weeks (Weaning Stage):** 
   - Feed **4 small meals daily** spaced evenly (e.g., 7:00 AM, 11:30 AM, 4:00 PM, 8:00 PM).
   - Soften premium puppy kibble with warm water or puppy milk replacer into a moist porridge.
2. **3 to 6 Months (Rapid Growth):** 
   - Reduce to **3 meals daily**.
   - Feed crunchy dry puppy kibble to promote jaw exercise and soothe teething gums.
3. **6 to 12 Months (Adolescence):** 
   - Transition to **2 meals daily** (morning & evening).
4. **12 Months (Adult Transition):** 
   - Gradually mix adult dog food over 7 days (25% -> 50% -> 75% -> 100%) to prevent digestive upset.

### ⚖️ Daily Portion & Practical Tips:
- **Measure by Weight:** Check the manufacturer feeding chart on your puppy kibble bag based on target adult weight. Split the total daily amount equally across meal times.
- **Hydration:** Keep fresh, clean water available in a shallow, tip-proof bowl 24/7.
- **Avoid Table Scraps:** Human seasonings, onions, garlic, and fatty trimmings cause severe gastrointestinal distress and pancreatitis.
- **Healthy Puppy Treats:** Use small pieces of boiled chicken breast, carrot coins, or single-ingredient training treats for positive reinforcement.','domain_expert_engine','2026-08-23 08:33:09.927270',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(9,'f206932e-3cb0-4776-89e8-408b673005ee','hello my cat is not eating','🐱 **Kitten & Cat Feeding Guidelines for your kitten **Is**:**

Cats are obligate carnivores requiring animal-based protein and essential amino acids like **Taurine** and **Arachidonic acid**.

### 📅 Kitten Feeding Stages:
- **4 to 8 Weeks:** Weaning phase. Mix canned kitten wet food with warm kitten formula into a soft puree 4-5 times daily.
- **2 to 6 Months:** Feed **3 to 4 portioned meals daily** of high-protein kitten formula. Wet food is strongly recommended to support healthy urinary tract hydration.
- **6 to 12 Months:** Feed 2-3 meals daily.
- **Adult Cats (1+ Years):** Feed **2 measured meals daily** (approx. 200-250 calories depending on weight and indoor activity).

### ⚠️ Essential Feline Nutrition Rules:
- **Never feed dog food to cats** (lacks sufficient taurine and vitamin A, leading to blindness and heart disease).
- **Cow''s milk is toxic** (most kittens and cats are lactose intolerant and develop painful diarrhea).','domain_expert_engine','2026-08-23 11:51:42.810476',2);
INSERT INTO "CHAT_HISTORY" VALUES(10,'f206932e-3cb0-4776-89e8-408b673005ee','she is 12 monts food remommend food to eat','🐾 Hello! I am your **Pet Care Companion AI Assistant**.

I am ready to help for your pet with:
- **Optimal Feeding Plans & Daily Portion Schedules** (Puppies, Kittens, Adults, Seniors)
- **Safe vs. Toxic Foods List**
- **Puppy/Kitten Potty & Behavioral Training**
- **Complete Vaccination & Preventive Deworming Schedules**
- **Coat Grooming & Hygiene Best Practices**
- **Breed Identification & Exercise Guidance**

*Ask me any specific question about your furry friend to get started!*','domain_expert_engine','2026-08-23 11:53:13.161515',2);
INSERT INTO "CHAT_HISTORY" VALUES(11,'guest','go to dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:30.488025',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(12,'guest','dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:30.492037',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(13,'guest','open my pets','🐾 **My Registered Pets Directory**

Manage your pet profiles, print digital ID cards, and access emergency medical records:

[🐾 Open My Pets](/pets/)

[➕ Register New Pet](/pets/add/)','PawPal Navigator','2026-10-07 17:51:30.495007',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(14,'guest','lost and found','🔍 **Lost & Found Pet Network**

Browse active community alerts for lost and found pets in your area with AI-verified police verification stamps:

[🔍 Open Lost & Found Network](/lostfound/)

[🚨 File Lost Pet Report](/lostfound/report/)','PawPal Navigator','2026-10-07 17:51:30.497343',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(15,'guest','smart recommend','⭐ **Smart Caretaker Recommendation Engine**

Find the highest-rated verified caretakers matching your pet''s breed requirements, experience, and daily workload limits:

[⭐ Open Smart Recommendations](/recommendations/)

[🏪 Browse All Caretakers](/marketplace/)','PawPal Navigator','2026-10-07 17:51:30.500444',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(16,'guest','detect breed','📸 **AI Pet Breed Scanner**

Upload any cat or dog photo to instantly identify their breed with deep learning computer vision:

[📸 Open AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:30.503930',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(17,'guest','profile','🐾 Hello! I am your **Pet Care Companion AI Assistant**.

I am ready to help for your pet with:
- **Optimal Feeding Plans & Daily Portion Schedules** (Puppies, Kittens, Adults, Seniors)
- **Safe vs. Toxic Foods List**
- **Puppy/Kitten Potty & Behavioral Training**
- **Complete Vaccination & Preventive Deworming Schedules**
- **Coat Grooming & Hygiene Best Practices**
- **Breed Identification & Exercise Guidance**

*Ask me any specific question about your furry friend to get started!*','PawPal Veterinary Intelligence','2026-10-07 17:51:32.562792',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(18,'guest','How to feed my puppy?','🐕 **Canine Nutrition & Feeding Guide for your dog:**

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
- **Strictly Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol sweetener, cooked bones, macadamia nuts.','PawPal Veterinary Intelligence','2026-10-07 17:51:34.600139',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(19,'guest','go to dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:51.051834',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(20,'guest','dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:51.054587',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(21,'guest','open my pets','🐾 **My Registered Pets Directory**

Manage your pet profiles, print digital ID cards, and access emergency medical records:

[🐾 Open My Pets](/pets/)

[➕ Register New Pet](/pets/add/)','PawPal Navigator','2026-10-07 17:51:51.057428',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(22,'guest','lost and found','🔍 **Lost & Found Pet Network**

Browse active community alerts for lost and found pets in your area with AI-verified police verification stamps:

[🔍 Open Lost & Found Network](/lostfound/)

[🚨 File Lost Pet Report](/lostfound/report/)','PawPal Navigator','2026-10-07 17:51:51.060118',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(23,'guest','smart recommend','⭐ **Smart Caretaker Recommendation Engine**

Find the highest-rated verified caretakers matching your pet''s breed requirements, experience, and daily workload limits:

[⭐ Open Smart Recommendations](/recommendations/)

[🏪 Browse All Caretakers](/marketplace/)','PawPal Navigator','2026-10-07 17:51:51.062345',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(24,'guest','detect breed','📸 **AI Pet Breed Scanner**

Upload any cat or dog photo to instantly identify their breed with deep learning computer vision:

[📸 Open AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:51.065743',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(25,'guest','profile','👤 **User Profile & Account Settings**

Update your personal information, contact numbers, address, and profile photo:

[👤 Go to My Profile](/users/profile/)','PawPal Navigator','2026-10-07 17:51:51.068388',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(26,'guest','bookings','📅 **Bookings & Appointments Manager**

View your scheduled pet care bookings, appointment statuses, and upcoming dates:

[📅 Open My Bookings](/bookings/my-bookings/)','PawPal Navigator','2026-10-07 17:51:51.072348',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(27,'guest','How to feed my puppy?','🐕 **Canine Nutrition & Feeding Guide for your dog:**

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
- **Strictly Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol sweetener, cooked bones, macadamia nuts.','PawPal Veterinary Intelligence','2026-10-07 17:51:53.128804',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(28,'guest','go to dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:51:59.717839',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(29,'guest','go to dashboard','🚀 **Navigating to Dashboard**

Click the direct button below to access your **Pet Care Dashboard**:

[📊 Open Dashboard](/users/dashboard/)

**Quick Platform Shortcuts:**
- [🐾 My Pets](/pets/)
- [🩺 Health Tracker](/health/reminders/)
- [🔍 Lost & Found Network](/lostfound/)
- [⭐ Smart Recommendations](/recommendations/)
- [📸 AI Breed Scanner](/breed-detection/)','PawPal Navigator','2026-10-07 17:52:06.198368',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(30,'guest','How to feed my puppy?','🐕 **Canine Nutrition & Feeding Guide for your dog:**

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
- **Strictly Toxic:** Chocolate, grapes, raisins, onions, garlic, xylitol sweetener, cooked bones, macadamia nuts.','PawPal Veterinary Intelligence','2026-10-07 17:52:08.251880',NULL);
INSERT INTO "CHAT_HISTORY" VALUES(35,'c5b4765e-f046-4119-b0f9-554ac20b2902','go to dash board','🚀 **Redirecting to Dashboard...**','PawPal Navigator','2026-10-07 18:11:56.255441',1);
INSERT INTO "CHAT_HISTORY" VALUES(37,'22818f51-c07f-421d-93e9-322f820fc04a','go to dashboard','🚀 **Redirecting to Dashboard...**','PawPal Navigator','2026-10-07 18:25:02.627039',10);
CREATE TABLE "HEALTH_RECORDS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "record_date" date NOT NULL, "condition_title" varchar(200) NOT NULL, "diagnosis" text NULL, "treatment_plan" text NULL, "vet_name" varchar(150) NULL, "clinic_name" varchar(200) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "HEALTH_RECORDS" VALUES(1,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Bruno is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.710764',5);
INSERT INTO "HEALTH_RECORDS" VALUES(2,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Luna is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.715870',6);
INSERT INTO "HEALTH_RECORDS" VALUES(3,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Coco is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.718434',7);
INSERT INTO "HEALTH_RECORDS" VALUES(4,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Rocky is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.720528',8);
INSERT INTO "HEALTH_RECORDS" VALUES(5,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Milo is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.728968',9);
INSERT INTO "HEALTH_RECORDS" VALUES(6,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Simba is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.744867',10);
INSERT INTO "HEALTH_RECORDS" VALUES(7,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Bella is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.757531',11);
INSERT INTO "HEALTH_RECORDS" VALUES(8,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Kiwi is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.769718',12);
INSERT INTO "HEALTH_RECORDS" VALUES(9,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Charlie is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.778433',13);
INSERT INTO "HEALTH_RECORDS" VALUES(10,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Oliver is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.786070',14);
INSERT INTO "HEALTH_RECORDS" VALUES(11,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Shadow is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.786070',15);
INSERT INTO "HEALTH_RECORDS" VALUES(12,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Lily is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.794251',16);
INSERT INTO "HEALTH_RECORDS" VALUES(13,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Bunbun is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.794251',17);
INSERT INTO "HEALTH_RECORDS" VALUES(14,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Daisy is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.802659',18);
INSERT INTO "HEALTH_RECORDS" VALUES(15,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Nala is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.802659',19);
INSERT INTO "HEALTH_RECORDS" VALUES(16,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Tyson is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.810788',20);
INSERT INTO "HEALTH_RECORDS" VALUES(17,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Oreo is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.819166',21);
INSERT INTO "HEALTH_RECORDS" VALUES(18,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Ginger is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.819166',22);
INSERT INTO "HEALTH_RECORDS" VALUES(19,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Rio is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.819166',23);
INSERT INTO "HEALTH_RECORDS" VALUES(20,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Cooper is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.827719',24);
INSERT INTO "HEALTH_RECORDS" VALUES(21,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Mia is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.836113',25);
INSERT INTO "HEALTH_RECORDS" VALUES(22,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Cheeku is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.838053',26);
INSERT INTO "HEALTH_RECORDS" VALUES(23,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Leo is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.844762',27);
INSERT INTO "HEALTH_RECORDS" VALUES(24,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Chloe is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.844762',28);
INSERT INTO "HEALTH_RECORDS" VALUES(25,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Buster is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.853404',29);
INSERT INTO "HEALTH_RECORDS" VALUES(26,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Penny is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.861827',30);
INSERT INTO "HEALTH_RECORDS" VALUES(27,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Casper is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.865840',31);
INSERT INTO "HEALTH_RECORDS" VALUES(28,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Pip is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.868112',32);
INSERT INTO "HEALTH_RECORDS" VALUES(29,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Thor is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.874496',33);
INSERT INTO "HEALTH_RECORDS" VALUES(30,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Stella is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.877929',34);
INSERT INTO "HEALTH_RECORDS" VALUES(31,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Fluffy is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.877929',35);
INSERT INTO "HEALTH_RECORDS" VALUES(32,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Zoe is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.894722',36);
INSERT INTO "HEALTH_RECORDS" VALUES(33,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Cookie is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.895835',37);
INSERT INTO "HEALTH_RECORDS" VALUES(34,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Bruno Jr is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.909084',38);
INSERT INTO "HEALTH_RECORDS" VALUES(35,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Ruby is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.910824',39);
INSERT INTO "HEALTH_RECORDS" VALUES(36,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Simba Cat is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.919206',40);
INSERT INTO "HEALTH_RECORDS" VALUES(37,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Sunny is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.928137',41);
INSERT INTO "HEALTH_RECORDS" VALUES(38,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Maximus is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.940919',42);
INSERT INTO "HEALTH_RECORDS" VALUES(39,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Snoopy is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.944756',43);
INSERT INTO "HEALTH_RECORDS" VALUES(40,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Snowball is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.953577',44);
INSERT INTO "HEALTH_RECORDS" VALUES(41,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Maya is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.961397',45);
INSERT INTO "HEALTH_RECORDS" VALUES(42,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Cleo is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.961397',46);
INSERT INTO "HEALTH_RECORDS" VALUES(43,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Rex is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.974227',47);
INSERT INTO "HEALTH_RECORDS" VALUES(44,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Penny Cat is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.977984',48);
INSERT INTO "HEALTH_RECORDS" VALUES(45,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Teddy is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.977984',49);
INSERT INTO "HEALTH_RECORDS" VALUES(46,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Hazel is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.991079',50);
INSERT INTO "HEALTH_RECORDS" VALUES(47,'2026-07-16','Annual Comprehensive Wellness Exam','Overall physiological parameters within normal limits. Mango is bright, alert, and responsive.','Continue balanced diet, preventive monthly parasite control, and daily exercise.','Dr. S. Sundaram BVSc','Tamil Nadu Pet Healthcare Hospital','2026-09-14 13:40:07.994276',51);
CREATE TABLE "LOST_PETS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "pet_name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "last_seen_location" varchar(255) NOT NULL, "date_lost" date NOT NULL, "description" text NULL, "contact_number" varchar(30) NOT NULL, "photo" varchar(100) NULL, "reward_amount" decimal NOT NULL, "status" varchar(25) NOT NULL, "created_at" datetime NOT NULL, "reporter_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "alternate_contact" varchar(50) NULL, "approx_age" varchar(50) NULL, "collar_description" varchar(200) NULL, "color_pattern" varchar(150) NULL, "contact_name" varchar(150) NULL, "distinctive_marks" text NULL, "gender" varchar(15) NOT NULL, "how_lost" text NULL, "microchip_id" varchar(100) NULL, "police_complaint_status" varchar(30) NOT NULL, "police_contact_details" varchar(200) NULL, "police_csr_number" varchar(100) NULL, "police_filing_date" date NULL, "police_station_name" varchar(200) NULL, "reunited_date" date NULL, "reunited_details" text NULL, "reward_details" varchar(255) NULL, "time_lost" varchar(100) NULL, "updated_at" datetime NOT NULL, "police_document" varchar(100) NULL, "police_verification_confidence" decimal NOT NULL, "police_verification_details" text NULL, "police_verified_at" datetime NULL, "police_verified_by_ai" bool NOT NULL);
INSERT INTO "LOST_PETS" VALUES(14,'Bruno','Dog','Golden Retriever','Besant Nagar Beach Promenade near 5th Avenue, Chennai, Tamil Nadu','2026-10-04','Extremely friendly, responds to whistle and the name "Bruno". Loves peanut butter treats. May be slightly anxious near heavy traffic.','+91 98401 23456','lost_pets/lost_bruno_14.jpg',10000,'SIGHTING_REPORTED','2026-10-07 17:28:21.773160',2,'+91 94440 98765 (Family)','3.0 years','Red reflective nylon collar with metal bell & engraved brass nametag "BRUNO"','Rich Honey Golden coat with white star blaze on chest','Rajesh Kumar (Owner)','Distinctive heart-shaped dark birthmark on inner left thigh, black spot on upper roof of mouth/tongue, docked tail, minor scar on right ear tip.','Male','Startled by sudden loud festival firecrackers near beach car parking; slipped leash and sprinted towards 4th Main Road.','981098102345678','FILED','Sub-Inspector V. Ramanathan (044-2491-XXXX / Desk: 044-2491-2345)','CSR No. 442/2026','2026-10-05','J-2 Adyar Police Station, Chennai',NULL,NULL,'₹10,000 Cash Reward - Guaranteed immediate payout upon safe return, no questions asked!','06:30 PM (Evening Walk)','2026-10-07 17:28:24.038550','police_docs/police_csr_bruno_14.jpg',75,'{"seal_detection": {"passed": true, "score": 100.0, "label": "Official Circular Ink Seal & Stamp", "status": "Verified"}, "header_verification": {"passed": true, "score": 40.0, "label": "Tamil Nadu Police Official Header", "status": "Verified"}, "csr_reference_match": {"passed": true, "score": 80.0, "label": "CSR Reference (CSR NO. 442/2026)", "status": "Matched"}, "station_jurisdiction": {"passed": true, "score": 80.0, "label": "Jurisdiction: J-2 Adyar Police Station, Chennai", "status": "Matched"}}','2026-10-07 17:28:24.038550',1);
INSERT INTO "LOST_PETS" VALUES(15,'Bella','Dog','Beagle','Anna Nagar Tower Park, Gate 3, 3rd Avenue, Chennai, Tamil Nadu','2026-10-05','Very energetic and food motivated. Responds to clicker and high-pitched voice. May approach people holding snacks.','+91 98840 55667','lost_pets/lost_bella_15.jpg',5000,'LOST','2026-10-07 17:28:21.790115',2,'+91 97910 11223','2.0 years','Purple floral patterned collar with silver bell and rubber GPS holder','Classic Tri-Color (Black saddle, tan legs & face, white chest & tail tip)','Priya Sridhar','Unique white clover-shaped patch on nape of neck, distinct freckled tan spots across snout, notched left ear tip.','Female','Followed a squirrel scent trail into dense hedge bushes; slipped harness while owner was tying shoelace.','985141002938475','FILED','Head Constable M. Selvam (044-2621-XXXX)','CSR No. 318/2026','2026-10-05','K-4 Anna Nagar Police Station, Chennai',NULL,NULL,'₹5,000 Cash Reward for safe return or verified sighting lead!','07:00 AM (Morning Jog)','2026-10-07 17:28:23.704489','police_docs/police_csr_bella_15.jpg',75,'{"seal_detection": {"passed": true, "score": 100.0, "label": "Official Circular Ink Seal & Stamp", "status": "Verified"}, "header_verification": {"passed": true, "score": 40.0, "label": "Tamil Nadu Police Official Header", "status": "Verified"}, "csr_reference_match": {"passed": true, "score": 80.0, "label": "CSR Reference (CSR NO. 318/2026)", "status": "Matched"}, "station_jurisdiction": {"passed": true, "score": 80.0, "label": "Jurisdiction: K-4 Anna Nagar Police Station, Chennai", "status": "Matched"}}','2026-10-07 17:28:23.704489',1);
INSERT INTO "LOST_PETS" VALUES(16,'Simba','Cat','Persian Cat','River View Enclave, Kotturpuram, Chennai, Tamil Nadu','2026-10-03','Indoor-only cat, likely hiding in quiet dry corners, under cars, or behind stairwells. Requires special hypoallergenic renal diet.','+91 98412 34567','lost_pets/lost_simba_16.jpg',7500,'LOST','2026-10-07 17:28:21.798123',2,'+91 98410 88990','2.5 years','Blue velvet breakaway collar with brass fish charm','Pure Snow White long fur, striking Heterochromia odd-eyes','Deepa Chandran','Striking Odd Eyes (Left eye deep cobalt blue, Right eye golden amber), small pink heart-shaped birthmark on left front paw pad, fluffy bottle-brush tail.','Male','Escaped through balcony sliding glass door accidentally left unlatched during rain shower; hopped down garden compound terrace.','RFID-TN-CHE-998821','FILED','Station Duty Officer (044-2235-XXXX)','Diary Entry #89 (CSR under verification)','2026-10-04','J-3 Guindy Police Station, Chennai',NULL,NULL,'₹7,500 Cash Reward - Simba needs daily medical care, please help us find him!','09:15 PM (Night)','2026-10-07 17:28:23.348389','police_docs/police_csr_simba_16.jpg',75,'{"seal_detection": {"passed": true, "score": 100.0, "label": "Official Circular Ink Seal & Stamp", "status": "Verified"}, "header_verification": {"passed": true, "score": 40.0, "label": "Tamil Nadu Police Official Header", "status": "Verified"}, "csr_reference_match": {"passed": true, "score": 80.0, "label": "CSR Reference (DIARY ENTRY #89 (CSR UNDER VERIFICATION))", "status": "Matched"}, "station_jurisdiction": {"passed": true, "score": 80.0, "label": "Jurisdiction: J-3 Guindy Police Station, Chennai", "status": "Matched"}}','2026-10-07 17:28:23.348389',1);
INSERT INTO "LOST_PETS" VALUES(17,'Thor','Dog','German Shepherd','Velachery Main Road near Phoenix Marketcity, Chennai, Tamil Nadu','2026-09-28','Command trained in English and Tamil (Sit, Stay, Come). Protective yet gentle with humans.','+91 99620 12345','lost_pets/lost_thor_17.jpg',15000,'REUNITED','2026-10-07 17:28:21.801074',2,'+91 98400 67890','3.5 years','Black tactical nylon collar with heavy-duty steel ring','Black & Rich Tan saddle coat with black facial mask','Vikram Seth','Tan diamond blaze mark above right brow, white patch under chin, distinctive double dewclaws on rear legs, strong athletic build.','Male','Jumped compound gate chasing stray cats after heavy thunderclap.','981098105554321','FILED','Sub-Inspector K. Murugesan (044-2244-XXXX)','CSR No. 512/2026 (Case Resolved)','2026-09-29','S-14 Velachery Police Station, Chennai','2026-10-02','Safely recovered after an observant security guard at Velachery MRTS station recognized Thor from our Pet Care Companion lost alert! The guard sheltered him overnight and contacted us. Thor was reunited with his overjoyed family without a scratch!','₹15,000 Cash Reward (Rewarded to MRTS security staff)','08:30 PM','2026-10-07 17:28:23.021201','police_docs/police_csr_thor_17.jpg',75,'{"seal_detection": {"passed": true, "score": 100.0, "label": "Official Circular Ink Seal & Stamp", "status": "Verified"}, "header_verification": {"passed": true, "score": 40.0, "label": "Tamil Nadu Police Official Header", "status": "Verified"}, "csr_reference_match": {"passed": true, "score": 80.0, "label": "CSR Reference (CSR NO. 512/2026 (CASE RESOLVED))", "status": "Matched"}, "station_jurisdiction": {"passed": true, "score": 80.0, "label": "Jurisdiction: S-14 Velachery Police Station, Chennai", "status": "Matched"}}','2026-10-07 17:28:23.020233',1);
INSERT INTO "LOST_PETS" VALUES(18,'Milo (Found Pet)','Dog','Indie / Indian Pariah Dog','Found near Pondy Bazaar Pedestrian Plaza, T. Nagar, Chennai, Tamil Nadu','2026-10-06','Extremely well-behaved, knows "shake hand" and "sit". Friendly with children and other dogs.','+91 98409 88776','lost_pets/lost_milo_18.jpg',0,'FOUND','2026-10-07 17:28:21.805114',2,'+91 99401 55443','1.5 years','Green canvas collar without nametag (collar worn recently)','Fawn tan coat with black muzzle and white chest star','Sneha Sundaram (Animal Rescuer / Foster)','Curled sickle tail with bright white tip, distinct dark circular birthmark behind right ear, very clean and friendly (clearly someone''s beloved pet).','Male','Found wandering confused near street vendors in busy traffic. Rescued and currently sheltered safely at foster home in T. Nagar. Looking for original owner!','No microchip detected during vet scan','NOT_FILED',NULL,'Community Sighting Alert #TN-091',NULL,'Blue Cross of India & Local T. Nagar Community Notice Filed',NULL,NULL,'No reward needed - Free handover upon showing pet ownership proof/photos','04:00 PM (Afternoon)','2026-10-07 17:28:21.805114','',0,NULL,NULL,0);
INSERT INTO "LOST_PETS" VALUES(19,'Luna','Dog','Siberian Husky','Race Course Walking Track / Redfields, Coimbatore, Tamil Nadu','2026-10-06','Very vocal, howls when hearing sirens. Friendly but energetic. Cannot tolerate hot sun; urgent search underway!','+91 94433 11223','lost_pets/lost_luna_19.jpg',12000,'LOST','2026-10-07 17:28:21.809070',2,'+91 98422 44556','2.5 years','Pink braided waterproof collar with stainless steel cylinder tag','Silver Grey and Snow White plush coat, Ice Blue Eyes','Dr. Arvind Balaji','Symmetrical butterfly facial mask, distinctive black nose with pink "snow nose" center streak, tiny notch on tip of left ear, very striking blue eyes.','Female','Slipped through automated sliding gate when delivery van entered compound; ran towards Race Course walking promenade.','981098776655443','FILED','Inspector S. Palanisamy (0422-222-XXXX)','CSR No. 209/2026','2026-10-07','B-4 Race Course Police Station, Coimbatore',NULL,NULL,'₹12,000 Cash Reward for safe return or direct information leading to recovery!','05:45 PM (Evening Walk)','2026-10-07 17:28:22.709923','police_docs/police_csr_luna_19.jpg',75,'{"seal_detection": {"passed": true, "score": 100.0, "label": "Official Circular Ink Seal & Stamp", "status": "Verified"}, "header_verification": {"passed": true, "score": 40.0, "label": "Tamil Nadu Police Official Header", "status": "Verified"}, "csr_reference_match": {"passed": true, "score": 80.0, "label": "CSR Reference (CSR NO. 209/2026)", "status": "Matched"}, "station_jurisdiction": {"passed": true, "score": 80.0, "label": "Jurisdiction: B-4 Race Course Police Station, Coimbatore", "status": "Matched"}}','2026-10-07 17:28:22.709923',1);
CREATE TABLE "LOST_PET_SIGHTINGS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "reporter_name" varchar(150) NOT NULL, "reporter_contact" varchar(100) NOT NULL, "sighting_location" varchar(255) NOT NULL, "sighting_date" date NOT NULL, "description" text NOT NULL, "photo" varchar(100) NULL, "created_at" datetime NOT NULL, "lost_pet_id" bigint NOT NULL REFERENCES "LOST_PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "sighting_time" varchar(50) NULL);
INSERT INTO "LOST_PET_SIGHTINGS" VALUES(8,'Ananya Sundaram','+91 98411 22334','Near Thalappakatti Restaurant, 2nd Avenue Besant Nagar','2026-10-05','Saw a golden retriever matching Bruno with red collar heading towards the beach road. Looked thirsty, drank water from a puddle.','','2026-10-07 17:28:21.781508',14,'08:15 PM');
INSERT INTO "LOST_PET_SIGHTINGS" VALUES(9,'Karthik Murugan','+91 97900 33445','Near Damodar Gardens Gate, Adyar','2026-10-06','Spotted wandering near tea stall. Very gentle, wagged tail when called Bruno but walked towards shaded garden lane.','','2026-10-07 17:28:21.786074',14,'07:30 AM');
INSERT INTO "LOST_PET_SIGHTINGS" VALUES(10,'Vignesh Parthasarathy','+91 98844 99887','Near Shanthi Colony Roundabout, Anna Nagar','2026-10-06','Saw a small tri-color beagle with purple collar sniffing near juice shop. Ran towards 4th avenue when a scooter honked.','','2026-10-07 17:28:21.793139',15,'06:45 PM');
CREATE TABLE "MATCH_PROFILES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bio" text NOT NULL, "looking_for" varchar(100) NOT NULL, "location" varchar(200) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL UNIQUE REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "MATCH_PROFILES" VALUES(1,'Max is an outgoing Golden who loves playing fetch and swimming. Looking for friendly park playmates on weekends!','Playmate & Walking Buddy','Zilker Park / Barton Springs',1,'2026-08-23 07:06:10.663627',1);
INSERT INTO "MATCH_PROFILES" VALUES(2,'Athletic German Shepherd looking for agility training companions and group hiking buddies.','Agility / Training Partner','South Austin Trail System',1,'2026-08-23 07:06:10.670885',3);
CREATE TABLE "MATCH_REQUESTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "message" varchar(500) NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "receiver_profile_id" bigint NOT NULL REFERENCES "MATCH_PROFILES" ("id") DEFERRABLE INITIALLY DEFERRED, "sender_profile_id" bigint NOT NULL REFERENCES "MATCH_PROFILES" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "MATCH_REQUESTS" VALUES(1,'Hi David! Would love to get Max and Rocky together for a playdate at the park this Saturday!','PENDING','2026-08-23 07:06:10.679186',2,1);
CREATE TABLE "MEDICINES" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "medicine_name" varchar(150) NOT NULL, "dosage" varchar(100) NOT NULL, "frequency" varchar(100) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "notes" text NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "MEDICINES" VALUES(1,'Probiotic GI Powder','1 scoop (5g)','Once daily mixed in wet food','2026-08-13','2026-09-12','Restores healthy intestinal gut flora',1,'2026-08-23 07:06:10.591898',2);
INSERT INTO "MEDICINES" VALUES(2,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.711397',5);
INSERT INTO "MEDICINES" VALUES(3,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.720528',8);
INSERT INTO "MEDICINES" VALUES(4,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.761632',11);
INSERT INTO "MEDICINES" VALUES(5,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.786070',14);
INSERT INTO "MEDICINES" VALUES(6,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.794251',17);
INSERT INTO "MEDICINES" VALUES(7,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.810788',20);
INSERT INTO "MEDICINES" VALUES(8,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.819166',23);
INSERT INTO "MEDICINES" VALUES(9,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.840908',26);
INSERT INTO "MEDICINES" VALUES(10,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.853404',29);
INSERT INTO "MEDICINES" VALUES(11,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.869902',32);
INSERT INTO "MEDICINES" VALUES(12,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.886260',35);
INSERT INTO "MEDICINES" VALUES(13,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.910824',38);
INSERT INTO "MEDICINES" VALUES(14,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.928137',41);
INSERT INTO "MEDICINES" VALUES(15,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.953577',44);
INSERT INTO "MEDICINES" VALUES(16,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.974227',47);
INSERT INTO "MEDICINES" VALUES(17,'NexGard Spectra Chewables','1 Chewable Tablet (Monthly)','Once every 30 days with food','2026-08-30','2027-02-26','Broad spectrum flea, tick, and heartworm prevention.',1,'2026-09-14 13:40:07.994276',50);
CREATE TABLE "NOTIFICATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(150) NOT NULL, "message" varchar(500) NOT NULL, "notification_type" varchar(30) NOT NULL, "link" varchar(255) NULL, "is_read" bool NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "NOTIFICATIONS" VALUES(1,'Vaccination Reminder Due Soon 💉','DHPP Core Vaccine for Max is due in 15 days (2026-09-07).','REMINDER','/health/reminders/',1,'2026-08-23 07:06:10.706802',2);
INSERT INTO "NOTIFICATIONS" VALUES(2,'New Booking Request! 🐾','David Miller requested a Dog Walking booking for Rocky on 2026-08-25.','BOOKING','/bookings/caretaker/requests/',0,'2026-08-23 07:06:10.715863',5);
INSERT INTO "NOTIFICATIONS" VALUES(3,'New Booking Request!','Akash Kumar requested a Pet Sitting booking for Coco (2026-10-20 to 2026-10-20).','BOOKING','/bookings/caretaker/requests/',0,'2026-10-17 18:17:31.579981',43);
INSERT INTO "NOTIFICATIONS" VALUES(4,'Booking Confirmed!','Your booking for Coco was accepted by Anandhi Muthukumar!','BOOKING','/bookings/my-bookings/',0,'2026-10-17 18:20:07.913687',10);
INSERT INTO "NOTIFICATIONS" VALUES(5,'Payment Confirmed!','Your payment of ₹2160.00 for booking #44 (Coco with Anandhi Muthukumar) is confirmed. Transaction ID: pay_test_44_10.','BOOKING','/bookings/44/payment/',0,'2026-10-17 18:48:07.448918',10);
INSERT INTO "NOTIFICATIONS" VALUES(6,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹2160.00 for booking #44 (Coco) via Razorpay.','BOOKING','/bookings/caretaker/requests/',1,'2026-10-17 18:48:07.461794',43);
INSERT INTO "NOTIFICATIONS" VALUES(7,'Booking Completed – Rate Your Experience','Your booking #44 is complete! Please leave a review for Anandhi Muthukumar.','BOOKING','/reviews/add/44/',0,'2026-10-17 19:09:28.172812',10);
INSERT INTO "NOTIFICATIONS" VALUES(8,'New Booking Request!','Akash Kumar requested a Overnight Boarding booking for Coco (2026-10-20 to 2026-10-21).','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 05:53:01.554071',43);
INSERT INTO "NOTIFICATIONS" VALUES(9,'Booking Confirmed!','Your booking for Coco was accepted by Anandhi Muthukumar!','BOOKING','/bookings/my-bookings/',0,'2026-10-18 05:54:55.597708',10);
INSERT INTO "NOTIFICATIONS" VALUES(10,'Payment Confirmed!','Your payment of ₹2160.00 for booking #44 (Coco with Anandhi Muthukumar) is confirmed. Transaction ID: pay_test_44_10.','BOOKING','/bookings/44/payment/',0,'2026-10-18 06:33:46.039845',10);
INSERT INTO "NOTIFICATIONS" VALUES(11,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹2160.00 for booking #44 (Coco) via Razorpay.','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 06:33:46.049754',43);
INSERT INTO "NOTIFICATIONS" VALUES(12,'Payment Confirmed!','Your payment of ₹4320.00 for booking #45 (Coco with Anandhi Muthukumar) is confirmed. Transaction ID: pay_test_45_10.','BOOKING','/bookings/45/payment/',0,'2026-10-18 06:40:56.484255',10);
INSERT INTO "NOTIFICATIONS" VALUES(13,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹4320.00 for booking #45 (Coco) via Razorpay.','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 06:40:56.492542',43);
INSERT INTO "NOTIFICATIONS" VALUES(14,'Payment Confirmed!','Your payment of ₹2160.00 for booking #44 (Coco with Anandhi Muthukumar) is confirmed. Transaction ID: pay_test_44_10.','BOOKING','/bookings/44/payment/',1,'2026-10-18 07:56:54.023105',10);
INSERT INTO "NOTIFICATIONS" VALUES(15,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹2160.00 for booking #44 (Coco) via Razorpay.','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 07:56:54.040732',43);
INSERT INTO "NOTIFICATIONS" VALUES(16,'Payment Confirmed!','Your payment of ₹1000.00 for booking #29 (Bruno with Priya Sharma) is confirmed. Transaction ID: pay_test_29_10.','BOOKING','/bookings/29/payment/',0,'2026-10-18 08:24:24.580525',10);
INSERT INTO "NOTIFICATIONS" VALUES(17,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹1000.00 for booking #29 (Bruno) via Razorpay.','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 08:24:24.592894',30);
INSERT INTO "NOTIFICATIONS" VALUES(18,'New Booking Request!','Akash Kumar requested a Daycare booking for Luna (2026-10-28 to 2026-10-28).','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 08:34:13.370260',32);
INSERT INTO "NOTIFICATIONS" VALUES(19,'Booking Confirmed!','Your booking for Luna was accepted by Karthikeyan Murugan!','BOOKING','/bookings/my-bookings/',0,'2026-10-18 10:38:18.155569',10);
INSERT INTO "NOTIFICATIONS" VALUES(20,'Payment Confirmed!','Your payment of ₹1800.00 for booking #46 (Luna with Karthikeyan Murugan) is confirmed. Transaction ID: pay_test_46_10.','BOOKING','/bookings/46/payment/',0,'2026-10-18 10:42:37.169813',10);
INSERT INTO "NOTIFICATIONS" VALUES(21,'Booking Fee Paid!','Akash Kumar has completed the payment of ₹1800.00 for booking #46 (Luna) via Razorpay.','BOOKING','/bookings/caretaker/requests/',0,'2026-10-18 10:42:37.185365',32);
CREATE TABLE "PAYMENTS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "razorpay_order_id" varchar(100) NULL, "razorpay_payment_id" varchar(100) NULL, "razorpay_signature" varchar(255) NULL, "amount" decimal NOT NULL, "currency" varchar(10) NOT NULL, "status" varchar(20) NOT NULL, "payment_method" varchar(50) NULL, "bank_transaction_id" varchar(100) NULL, "error_code" varchar(100) NULL, "error_description" text NULL, "paid_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "booking_id" bigint NOT NULL UNIQUE REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "PAYMENTS" VALUES(2,'order_test_45_954ccbb236','pay_test_45_10','77de51f29144aa8d92239c5a6ed84db5c84bda50e6332892b27e373e390308ad',4320,'INR','SUCCESS','UPI (Google Pay Instant 1-Click)',NULL,NULL,NULL,'2026-10-18 06:40:56.457675','2026-10-18 05:55:09.525519','2026-10-18 06:40:56.457675',45);
INSERT INTO "PAYMENTS" VALUES(3,'order_test_44_8aa1c13e25','pay_test_44_10','d63a4dbddda2e832f9e65ba2bdaa0209f7d65af9dc0b19c8da7dbed9a4630082',2160,'INR','PENDING','UPI (Google Pay - customer01@okaxis)',NULL,NULL,NULL,'2026-10-18 07:56:53.978061','2026-10-18 06:41:38.172641','2026-10-18 11:33:01.363702',44);
INSERT INTO "PAYMENTS" VALUES(4,'order_test_29_94b1f9e6e5','pay_test_29_10','53093e13c06a95f84be76659f2837774f167737df083f6007ea8fe1e0c20ad89',1000,'INR','SUCCESS','UPI (Google Pay - customer01@okaxis)',NULL,NULL,NULL,'2026-10-18 08:24:24.538744','2026-10-18 08:00:08.004540','2026-10-18 08:24:24.540257',29);
INSERT INTO "PAYMENTS" VALUES(5,'order_test_46_8b0eca36be','pay_test_46_10','ca86d32ed786b7546de4d19cc9681c5bd3b98ed7ba29bf1145e1eded5a5a475f',1800,'INR','SUCCESS','Google Pay (Simulated Mobile QR Approval)',NULL,NULL,NULL,'2026-10-18 10:42:37.139723','2026-10-18 10:38:58.583867','2026-10-18 10:42:37.139723',46);
CREATE TABLE "PETS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "species" varchar(30) NOT NULL, "breed" varchar(100) NOT NULL, "age" decimal NOT NULL, "gender" varchar(10) NOT NULL, "weight" decimal NOT NULL, "health_condition" varchar(100) NOT NULL, "activity_level" varchar(20) NOT NULL, "vaccination_status" varchar(20) NOT NULL, "allergies" varchar(255) NULL, "medical_notes" text NULL, "photo" varchar(100) NULL, "qr_code" varchar(100) NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "owner_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "PETS" VALUES(1,'Max','Dog','Golden Retriever',3.5,'Male',31,'Healthy','High','Up to Date','None','Loves fetch in the lake! Microchipped #9851410029384.','','qrcodes/qr_pet_1_max.png','2026-08-23 07:06:10.177214','2026-08-23 07:06:10.177214',2);
INSERT INTO "PETS" VALUES(2,'Luna','Cat','Persian Cat',2,'Female',4.2,'Sensitive Stomach / Allergies','Low','Up to Date','Chicken & Dairy protein','Daily coat brushing required. Indoor only.','','qrcodes/qr_pet_2_luna.png','2026-08-23 07:06:10.452901','2026-08-23 07:06:10.452901',2);
INSERT INTO "PETS" VALUES(3,'Rocky','Dog','German Shepherd',4,'Male',36.5,'Healthy','Very High','Due Soon','None','Very obedient. Protects family backyard.','','qrcodes/qr_pet_3_rocky.png','2026-08-23 07:06:10.475321','2026-08-23 07:06:10.475321',3);
INSERT INTO "PETS" VALUES(4,'Bella','Dog','French Bulldog',2.5,'Female',12,'Overweight','Low','Up to Date','Beef','Avoid overheating during hot afternoons.','','qrcodes/qr_pet_4_bella.png','2026-08-23 07:06:10.497819','2026-08-23 07:06:10.497819',4);
INSERT INTO "PETS" VALUES(5,'Bruno','Dog','Labrador Retriever',3,'Male',28.5,'Healthy','High','Up to Date','None','Very active and loves fetching tennis balls.','pets/pet_001.jpg','qrcodes/qr_pet_5_bruno.png','2026-09-14 13:40:06.916947','2026-09-14 13:41:01.490321',10);
INSERT INTO "PETS" VALUES(6,'Luna','Cat','Persian Cat',2,'Female',4.2,'Healthy','Low','Up to Date','Dust sensitivity','Prefers quiet cozy corners and daily combing.','pets/pet_002.jpg','qrcodes/qr_pet_6_luna.png','2026-09-14 13:40:06.942031','2026-09-14 13:41:01.491433',10);
INSERT INTO "PETS" VALUES(7,'Coco','Rabbit','Holland Lop',1,'Female',1.8,'Healthy','Moderate','Up to Date','None','Loves fresh coriander and timothy hay.','pets/pet_003.jpg','qrcodes/qr_pet_7_coco.png','2026-09-14 13:40:06.952395','2026-09-14 13:41:01.492062',10);
INSERT INTO "PETS" VALUES(8,'Rocky','Dog','German Shepherd',4.5,'Male',34,'Healthy','Very High','Up to Date','None','Trained in basic obedience and agility.','pets/pet_004.jpg','qrcodes/qr_pet_8_rocky.png','2026-09-14 13:40:06.975039','2026-09-14 13:41:01.492683',11);
INSERT INTO "PETS" VALUES(9,'Milo','Cat','Siamese Cat',1.5,'Male',3.8,'Healthy','Moderate','Due Soon','None','Very vocal and affectionate cat.','pets/pet_005.jpg','qrcodes/qr_pet_9_milo.png','2026-09-14 13:40:06.989219','2026-09-14 13:41:01.493316',11);
INSERT INTO "PETS" VALUES(10,'Simba','Dog','Golden Retriever',2.5,'Male',30,'Healthy','High','Up to Date','Chicken allergy','Feed hypoallergenic salmon formula only.','pets/pet_006.jpg','qrcodes/qr_pet_10_simba.png','2026-09-14 13:40:06.999814','2026-09-14 13:41:01.494545',12);
INSERT INTO "PETS" VALUES(11,'Bella','Dog','Beagle',3,'Female',12,'Healthy','High','Up to Date','None','Loves scent tracking games and belly rubs.','pets/pet_007.jpg','qrcodes/qr_pet_11_bella.png','2026-09-14 13:40:07.008010','2026-09-14 13:41:01.495224',12);
INSERT INTO "PETS" VALUES(12,'Kiwi','Bird','Cockatiel',1.2,'Male',0.1,'Healthy','Low','Up to Date','None','Whistles tunes when music is playing.','pets/pet_008.jpg','qrcodes/qr_pet_12_kiwi.png','2026-09-14 13:40:07.015610','2026-09-14 13:41:01.496418',12);
INSERT INTO "PETS" VALUES(13,'Charlie','Dog','Pug',4,'Male',9.5,'Healthy','Low','Overdue','None','Needs facial wrinkle cleaning twice a week.','pets/pet_009.jpg','qrcodes/qr_pet_13_charlie.png','2026-09-14 13:40:07.024113','2026-09-14 13:41:01.497840',13);
INSERT INTO "PETS" VALUES(14,'Oliver','Cat','British Shorthair',2.8,'Male',5.5,'Healthy','Low','Up to Date','None','Calm and dignified lap cat.','pets/pet_010.jpg','qrcodes/qr_pet_14_oliver.png','2026-09-14 13:40:07.040595','2026-09-14 13:41:01.499024',13);
INSERT INTO "PETS" VALUES(15,'Shadow','Dog','Indie',2,'Male',18,'Healthy','Very High','Up to Date','None','Rescued street pup, very resilient and agile.','pets/pet_011.jpg','qrcodes/qr_pet_15_shadow.png','2026-09-14 13:40:07.049535','2026-09-14 13:41:01.499547',14);
INSERT INTO "PETS" VALUES(16,'Lily','Cat','Maine Coon',3.5,'Female',6.8,'Healthy','Moderate','Up to Date','None','Gentle giant with a thick winter coat.','pets/pet_012.jpg','qrcodes/qr_pet_16_lily.png','2026-09-14 13:40:07.056863','2026-09-14 13:41:01.500113',14);
INSERT INTO "PETS" VALUES(17,'Bunbun','Rabbit','Mini Rex',1.5,'Female',2.1,'Healthy','Moderate','Up to Date','None','Soft velvet coat, likes cardboard tunnels.','pets/pet_013.jpg','qrcodes/qr_pet_17_bunbun.png','2026-09-14 13:40:07.065241','2026-09-14 13:41:01.500734',14);
INSERT INTO "PETS" VALUES(18,'Daisy','Dog','Shih Tzu',2,'Female',6.2,'Healthy','Moderate','Up to Date','None','Requires daily eye wiping and gentle coat brushing.','pets/pet_014.jpg','qrcodes/qr_pet_18_daisy.png','2026-09-14 13:40:07.083965','2026-09-14 13:41:01.501987',15);
INSERT INTO "PETS" VALUES(19,'Nala','Cat','Indie Cat',1,'Female',3.2,'Healthy','Moderate','Up to Date','None','Loves watching birds through the window.','pets/pet_015.jpg','qrcodes/qr_pet_19_nala.png','2026-09-14 13:40:07.099341','2026-09-14 13:41:01.501987',15);
INSERT INTO "PETS" VALUES(20,'Tyson','Dog','Rottweiler',3.5,'Male',42,'Healthy','High','Up to Date','None','Loyal guard companion, very gentle with family.','pets/pet_016.jpg','qrcodes/qr_pet_20_tyson.png','2026-09-14 13:40:07.119319','2026-09-14 13:41:01.503006',16);
INSERT INTO "PETS" VALUES(21,'Oreo','Dog','Border Collie',2,'Male',19.5,'Healthy','Very High','Up to Date','None','Loves frisbee catches and obstacle courses.','pets/pet_017.jpg','qrcodes/qr_pet_21_oreo.png','2026-09-14 13:40:07.130327','2026-09-14 13:41:01.504014',16);
INSERT INTO "PETS" VALUES(22,'Ginger','Cat','Tabby Cat',2.2,'Female',4,'Healthy','Moderate','Up to Date','None','Loves chasing laser pointer dots.','pets/pet_018.jpg','qrcodes/qr_pet_22_ginger.png','2026-09-14 13:40:07.139706','2026-09-14 13:41:01.504014',17);
INSERT INTO "PETS" VALUES(23,'Rio','Bird','Lovebird',0.8,'Male',0.05,'Healthy','Low','Up to Date','None','Very active and chirps in the morning.','pets/pet_019.jpg','qrcodes/qr_pet_23_rio.png','2026-09-14 13:40:07.152485','2026-09-14 13:41:01.504014',17);
INSERT INTO "PETS" VALUES(24,'Cooper','Dog','Cocker Spaniel',3.2,'Male',13.5,'Healthy','High','Up to Date','Ear sensitivity','Keep ears clean and dry after baths.','pets/pet_020.jpg','qrcodes/qr_pet_24_cooper.png','2026-09-14 13:40:07.170107','2026-09-14 13:41:01.506023',18);
INSERT INTO "PETS" VALUES(25,'Mia','Cat','Ragdoll',1.8,'Female',4.8,'Healthy','Low','Due Soon','None','Limp and relaxed when held.','pets/pet_021.jpg','qrcodes/qr_pet_25_mia.png','2026-09-14 13:40:07.188737','2026-09-14 13:41:01.506023',18);
INSERT INTO "PETS" VALUES(26,'Cheeku','Rabbit','Netherland Dwarf',1,'Male',1.2,'Healthy','Moderate','Up to Date','None','Compact bunny, likes apple wood chews.','pets/pet_022.jpg','qrcodes/qr_pet_26_cheeku.png','2026-09-14 13:40:07.196781','2026-09-14 13:41:01.506023',18);
INSERT INTO "PETS" VALUES(27,'Leo','Dog','Pomeranian',4,'Male',4.5,'Healthy','Moderate','Up to Date','None','Fluffy coat and alert barker.','pets/pet_023.jpg','qrcodes/qr_pet_27_leo.png','2026-09-14 13:40:07.215353','2026-09-14 13:41:01.508031',19);
INSERT INTO "PETS" VALUES(28,'Chloe','Cat','Birman',2.5,'Female',4.1,'Healthy','Low','Up to Date','None','Gentle sapphire-eyed beauty.','pets/pet_024.jpg','qrcodes/qr_pet_28_chloe.png','2026-09-14 13:40:07.229603','2026-09-14 13:41:01.508031',19);
INSERT INTO "PETS" VALUES(29,'Buster','Dog','Boxer',3,'Male',30.5,'Healthy','High','Up to Date','None','Playful and loves jumping on trampoline.','pets/pet_025.jpg','qrcodes/qr_pet_29_buster.png','2026-09-14 13:40:07.246389','2026-09-14 13:41:01.508031',20);
INSERT INTO "PETS" VALUES(30,'Penny','Dog','Dachshund',2.5,'Female',8,'Healthy','Moderate','Up to Date','None','Avoid stairs to protect spine.','pets/pet_026.jpg','qrcodes/qr_pet_30_penny.png','2026-09-14 13:40:07.264998','2026-09-14 13:41:01.508031',20);
INSERT INTO "PETS" VALUES(31,'Casper','Cat','Russian Blue',2,'Male',4.5,'Healthy','Moderate','Up to Date','None','Silver shimmer coat, quiet companion.','pets/pet_027.jpg','qrcodes/qr_pet_31_casper.png','2026-09-14 13:40:07.285816','2026-09-14 13:41:01.508031',21);
INSERT INTO "PETS" VALUES(32,'Pip','Bird','Budgerigar',1,'Male',0.04,'Healthy','Low','Up to Date','None','Bright yellow budgie with cheerful chirps.','pets/pet_028.jpg','qrcodes/qr_pet_32_pip.png','2026-09-14 13:40:07.295577','2026-09-14 13:41:01.508031',21);
INSERT INTO "PETS" VALUES(33,'Thor','Dog','Siberian Husky',2.8,'Male',24,'Healthy','Very High','Up to Date','None','High energy, requires cool indoor space in summer.','pets/pet_029.jpg','qrcodes/qr_pet_33_thor.png','2026-09-14 13:40:07.312361','2026-09-14 13:41:01.512404',22);
INSERT INTO "PETS" VALUES(34,'Stella','Dog','Great Dane',3.5,'Female',52,'Healthy','Moderate','Up to Date','None','Gentle giant who thinks she is a lapdog.','pets/pet_030.jpg','qrcodes/qr_pet_34_stella.png','2026-09-14 13:40:07.320695','2026-09-14 13:41:01.512404',22);
INSERT INTO "PETS" VALUES(35,'Fluffy','Rabbit','Angora Rabbit',1.2,'Female',2.5,'Healthy','Low','Up to Date','None','Long wool requires weekly gentle grooming.','pets/pet_031.jpg','qrcodes/qr_pet_35_fluffy.png','2026-09-14 13:40:07.328669','2026-09-14 13:41:01.512404',22);
INSERT INTO "PETS" VALUES(36,'Zoe','Cat','Sphynx',3,'Female',3.6,'Healthy','High','Up to Date','Cold sensitivity','Keep indoors with warm sweaters during winter.','pets/pet_032.jpg','qrcodes/qr_pet_36_zoe.png','2026-09-14 13:40:07.345303','2026-09-14 13:41:01.512404',23);
INSERT INTO "PETS" VALUES(37,'Cookie','Cat','Scottish Fold',1.5,'Female',3.9,'Healthy','Low','Up to Date','None','Folded ears and sweet temperament.','pets/pet_033.jpg','qrcodes/qr_pet_37_cookie.png','2026-09-14 13:40:07.360408','2026-09-14 13:41:01.512404',23);
INSERT INTO "PETS" VALUES(38,'Bruno Jr','Dog','Doberman',2.2,'Male',36,'Healthy','Very High','Up to Date','None','Alert, highly trainable and intelligent.','pets/pet_034.jpg','qrcodes/qr_pet_38_bruno_jr.png','2026-09-14 13:40:07.377747','2026-09-14 13:41:01.512404',24);
INSERT INTO "PETS" VALUES(39,'Ruby','Dog','Cavalier King Charles',1.8,'Female',7.2,'Healthy','Moderate','Up to Date','None','Loving lap dog with silky ears.','pets/pet_035.jpg','qrcodes/qr_pet_39_ruby.png','2026-09-14 13:40:07.397374','2026-09-14 13:41:01.512404',24);
INSERT INTO "PETS" VALUES(40,'Simba Cat','Cat','Bengal Cat',2,'Male',5.2,'Healthy','High','Up to Date','None','Leopard spotted coat and very agile climber.','pets/pet_036.jpg','qrcodes/qr_pet_40_simba_cat.png','2026-09-14 13:40:07.410972','2026-09-14 13:41:01.512404',25);
INSERT INTO "PETS" VALUES(41,'Sunny','Bird','Sun Conure',1.5,'Male',0.12,'Healthy','Moderate','Up to Date','None','Vibrant orange and yellow feathers.','pets/pet_037.jpg','qrcodes/qr_pet_41_sunny.png','2026-09-14 13:40:07.425285','2026-09-14 13:41:01.512404',25);
INSERT INTO "PETS" VALUES(42,'Maximus','Dog','Labrador Retriever',4,'Male',31,'Healthy','High','Up to Date','None','Loves swimming in lakes and retrieving sticks.','pets/pet_038.jpg','qrcodes/qr_pet_42_maximus.png','2026-09-14 13:40:07.427299','2026-09-14 13:41:01.512404',26);
INSERT INTO "PETS" VALUES(43,'Snoopy','Dog','Beagle',2,'Male',11.5,'Healthy','High','Due Soon','None','Always following scent trails.','pets/pet_039.jpg','qrcodes/qr_pet_43_snoopy.png','2026-09-14 13:40:07.443682','2026-09-14 13:41:01.520843',26);
INSERT INTO "PETS" VALUES(44,'Snowball','Rabbit','Flemish Giant',2,'Female',4.8,'Healthy','Low','Up to Date','None','Calm giant rabbit, loves leafy greens.','pets/pet_040.jpg','qrcodes/qr_pet_44_snowball.png','2026-09-14 13:40:07.453251','2026-09-14 13:41:01.520843',26);
INSERT INTO "PETS" VALUES(45,'Maya','Dog','Indie',1.5,'Female',16.5,'Healthy','High','Up to Date','None','Very smart, rescued from Coimbatore.','pets/pet_041.jpg','qrcodes/qr_pet_45_maya.png','2026-09-14 13:40:07.459660','2026-09-14 13:41:01.520843',27);
INSERT INTO "PETS" VALUES(46,'Cleo','Cat','Bombay Cat',2.5,'Female',3.9,'Healthy','Moderate','Up to Date','None','Sleek black panther look with copper eyes.','pets/pet_042.jpg','qrcodes/qr_pet_46_cleo.png','2026-09-14 13:40:07.471557','2026-09-14 13:41:01.520843',27);
INSERT INTO "PETS" VALUES(47,'Rex','Dog','German Shepherd',3.8,'Male',35.5,'Healthy','Very High','Up to Date','None','Trained protection and family companion.','pets/pet_043.jpg','qrcodes/qr_pet_47_rex.png','2026-09-14 13:40:07.475669','2026-09-14 13:41:01.520843',28);
INSERT INTO "PETS" VALUES(48,'Penny Cat','Cat','Norwegian Forest Cat',3,'Female',6,'Healthy','Moderate','Up to Date','None','Dense water-resistant coat and bushy tail.','pets/pet_044.jpg','qrcodes/qr_pet_48_penny_cat.png','2026-09-14 13:40:07.492519','2026-09-14 13:41:01.520843',28);
INSERT INTO "PETS" VALUES(49,'Teddy','Dog','Poodle',2,'Male',7,'Healthy','High','Up to Date','None','Hypoallergenic curly coat, loves agility runs.','pets/pet_045.jpg','qrcodes/qr_pet_49_teddy.png','2026-09-14 13:40:07.508028','2026-09-14 13:41:01.520843',29);
INSERT INTO "PETS" VALUES(50,'Hazel','Cat','Abyssinian',1.8,'Female',3.5,'Healthy','High','Up to Date','None','Ruddy ticked coat and energetic jumper.','pets/pet_046.jpg','qrcodes/qr_pet_50_hazel.png','2026-09-14 13:40:07.518227','2026-09-14 13:41:01.520843',29);
INSERT INTO "PETS" VALUES(51,'Mango','Bird','African Grey',4,'Male',0.4,'Healthy','Low','Up to Date','None','Remarkable vocabulary and mimicry skills.','pets/pet_047.jpg','qrcodes/qr_pet_51_mango.png','2026-09-14 13:40:07.524725','2026-09-14 13:41:01.520843',29);
INSERT INTO "PETS" VALUES(52,'Milo','Dog','Golden Retriever',3,'Male',29,'Healthy','High','Up to Date','None','Friendly golden retriever.','','qrcodes/qr_pet_52_milo.png','2026-10-01 23:52:46.298940','2026-10-01 23:52:46.298940',9);
INSERT INTO "PETS" VALUES(53,'Daisy','Dog','Beagle',2,'Female',11,'Healthy','Moderate','Up to Date','None','Loves backyard fetch.','','qrcodes/qr_pet_53_daisy.png','2026-10-01 23:52:46.928777','2026-10-01 23:52:46.929792',9);
CREATE TABLE "RECOMMENDATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "input_breed" varchar(100) NOT NULL, "input_age" decimal NOT NULL, "input_weight" decimal NOT NULL, "input_health" varchar(100) NOT NULL, "input_activity" varchar(50) NOT NULL, "diet_category" varchar(150) NOT NULL, "recommended_food" varchar(200) NOT NULL, "recommended_service" varchar(200) NOT NULL, "care_tip" text NOT NULL, "created_at" datetime NOT NULL, "pet_id" bigint NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "RECOMMENDATIONS" VALUES(1,'Scottish Terrier',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 08:55:53.710160',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(2,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 09:26:40.878008',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(3,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 09:27:15.412623',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(4,'Persian Cat',2,4.2,'Sensitive Stomach / Allergies','Low','Hypoallergenic Single-Source Protein & Grain-Free','Farmina N&D Ocean Grain-Free Hypoallergenic Formula','Specialized Medical Monitoring & Controlled Diet Feeding','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:48.481071',2,2);
INSERT INTO "RECOMMENDATIONS" VALUES(5,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:49.345188',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(6,'Golden Retriever',3.5,31,'Healthy','High','Active Performance & Muscle Fuel (30/20 High Energy)','Orijen Amazing Grains High-Protein Energy Feast','High-Energy Active Adventure & Agility Exercise','Golden Retriever possesses high working stamina! Engage in 60-90 minutes of vigorous daily exercise, agility courses, and mental puzzle feeders.','2026-08-23 11:50:49.538349',1,2);
INSERT INTO "RECOMMENDATIONS" VALUES(7,'Persian Cat',2,4.2,'Sensitive Stomach / Allergies','Low','Hypoallergenic Single-Source Protein & Grain-Free','Farmina N&D Ocean Grain-Free Hypoallergenic Formula','Specialized Medical Monitoring & Controlled Diet Feeding','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:49.824647',2,2);
INSERT INTO "RECOMMENDATIONS" VALUES(8,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:50.064922',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(9,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:50.230857',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(10,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:50.414758',NULL,2);
INSERT INTO "RECOMMENDATIONS" VALUES(11,'Persian Cat',2,4.2,'Sensitive Stomach / Allergies','Low','Hypoallergenic Single-Source Protein & Grain-Free','Farmina N&D Ocean Grain-Free Hypoallergenic Formula','Specialized Medical Monitoring & Controlled Diet Feeding','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:56.306449',2,2);
INSERT INTO "RECOMMENDATIONS" VALUES(12,'Persian Cat',2,4.2,'Sensitive Stomach / Allergies','Low','Hypoallergenic Single-Source Protein & Grain-Free','Farmina N&D Ocean Grain-Free Hypoallergenic Formula','Specialized Medical Monitoring & Controlled Diet Feeding','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-08-23 11:50:59.462925',2,2);
INSERT INTO "RECOMMENDATIONS" VALUES(13,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-09-14 13:04:16.570848',NULL,9);
INSERT INTO "RECOMMENDATIONS" VALUES(14,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-09-14 13:04:16.611394',NULL,9);
INSERT INTO "RECOMMENDATIONS" VALUES(15,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-09-14 13:09:24.093191',NULL,9);
INSERT INTO "RECOMMENDATIONS" VALUES(16,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:04:31.621628',NULL,10);
INSERT INTO "RECOMMENDATIONS" VALUES(17,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:04:31.945024',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(18,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:04:36.704657',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(19,'Holland Lop',1,1.8,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:05:31.614095',7,10);
INSERT INTO "RECOMMENDATIONS" VALUES(20,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:05:46.539152',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(21,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 20:06:08.780226',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(22,'Labrador Retriever',3,28.5,'Healthy','High','Active Performance & Muscle Fuel (30/20 High Energy)','Orijen Amazing Grains High-Protein Energy Feast','High-Energy Active Adventure & Agility Exercise','Labrador Retriever possesses high working stamina! Engage in 60-90 minutes of vigorous daily exercise, agility courses, and mental puzzle feeders.','2026-10-01 23:55:24.276461',5,10);
INSERT INTO "RECOMMENDATIONS" VALUES(23,'Labrador Retriever',3,28,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 23:55:24.345194',NULL,10);
INSERT INTO "RECOMMENDATIONS" VALUES(24,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 23:55:48.340266',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(25,'Persian Cat',2,4.2,'Healthy','Low','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 23:55:49.924545',6,10);
INSERT INTO "RECOMMENDATIONS" VALUES(26,'Labrador Retriever',3,28.5,'Healthy','High','Active Performance & Muscle Fuel (30/20 High Energy)','Orijen Amazing Grains High-Protein Energy Feast','High-Energy Active Adventure & Agility Exercise','Labrador Retriever possesses high working stamina! Engage in 60-90 minutes of vigorous daily exercise, agility courses, and mental puzzle feeders.','2026-10-01 23:56:49.947588',5,10);
INSERT INTO "RECOMMENDATIONS" VALUES(27,'Holland Lop',1,1.8,'Healthy','Moderate','Daily Complete Balanced Adult Maintenance','Blue Buffalo Life Protection Natural Adult Blend','Standard Boarding & Daily Enrichment Walking','Maintain balanced twice-daily feeding, brush teeth weekly, and ensure fresh water is available 24/7.','2026-10-01 23:56:58.929341',7,10);
CREATE TABLE "REVIEWS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), "comment" text NOT NULL, "created_at" datetime NOT NULL, "booking_id" bigint NOT NULL UNIQUE REFERENCES "BOOKINGS" ("id") DEFERRABLE INITIALLY DEFERRED, "caretaker_id" bigint NOT NULL REFERENCES "CARETAKERS" ("id") DEFERRABLE INITIALLY DEFERRED, "reviewer_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "REVIEWS" VALUES(1,5,'Alex was phenomenal! Sent multiple daily photo updates of Max playing in the yard. Highly recommended!','2026-08-23 07:06:10.612760',1,1,2);
INSERT INTO "REVIEWS" VALUES(2,5,'Exceptional care! My pet was extremely happy and relaxed upon return. Highly recommended! (Bruno was so happy with Priya!)','2026-09-14 13:40:07.614679',4,5,10);
INSERT INTO "REVIEWS" VALUES(3,5,'Very punctual, caring, and communicative with constant photo updates. Will book again! (Luna was so happy with Priya!)','2026-09-14 13:40:07.620245',5,5,10);
INSERT INTO "REVIEWS" VALUES(4,4,'Great sitter, followed all feeding and walking instructions carefully. (Rocky was so happy with Priya!)','2026-09-14 13:40:07.625526',6,5,11);
INSERT INTO "REVIEWS" VALUES(5,5,'Outstanding service! Treated my pet like family. Could not ask for better care. (Simba was so happy with Suresh!)','2026-09-14 13:40:07.632297',7,6,12);
INSERT INTO "REVIEWS" VALUES(6,4,'Very knowledgeable and gentle with large energetic dogs. Excellent experience. (Charlie was so happy with Suresh!)','2026-09-14 13:40:07.636321',8,6,13);
INSERT INTO "REVIEWS" VALUES(7,5,'Super responsive and attentive to medical schedules. Top-tier caretaker! (Shadow was so happy with Karthikeyan!)','2026-09-14 13:40:07.641441',9,7,14);
INSERT INTO "REVIEWS" VALUES(8,5,'My cat adored her! Clean, stress-free environment and regular grooming. (Daisy was so happy with Deepa!)','2026-09-14 13:40:07.643451',10,8,15);
INSERT INTO "REVIEWS" VALUES(9,4,'Punctual and reliable for daily walking sessions. Very satisfied. (Tyson was so happy with Ramesh!)','2026-09-14 13:40:07.646412',11,9,16);
INSERT INTO "REVIEWS" VALUES(10,5,'The best pet sitting experience in Tamil Nadu. 5 stars all the way! (Ginger was so happy with Preethi!)','2026-09-14 13:40:07.646412',12,10,17);
INSERT INTO "REVIEWS" VALUES(11,4,'Warm and welcoming family environment. Our dog loved the open play yard. (Cooper was so happy with Manikandan!)','2026-09-14 13:40:07.653565',13,11,18);
INSERT INTO "REVIEWS" VALUES(12,5,'Professional, certified, and incredibly kind. Took great care of Bruno. (Leo was so happy with Gowri!)','2026-09-14 13:40:07.654605',14,12,19);
INSERT INTO "REVIEWS" VALUES(13,5,'Detailed daily reports and GPS walk tracking were fantastic. (Buster was so happy with Revathi!)','2026-09-14 13:40:07.654605',15,13,20);
INSERT INTO "REVIEWS" VALUES(14,4,'Friendly caretaker who easily handled our energetic pup. (Casper was so happy with Ashok!)','2026-09-14 13:40:07.654605',16,14,21);
INSERT INTO "REVIEWS" VALUES(15,5,'Wonderful overnight boarding. Pet came home clean, energized, and happy! (Thor was so happy with Bhuvaneshwari!)','2026-09-14 13:40:07.663115',17,15,22);
INSERT INTO "REVIEWS" VALUES(16,4,'Reliable and trustworthy. Handled medication flawlessly. (Zoe was so happy with Vignesh!)','2026-09-14 13:40:07.663115',18,16,23);
INSERT INTO "REVIEWS" VALUES(17,5,'Exceptional care! My pet was extremely happy and relaxed upon return. Highly recommended! (Bruno Jr was so happy with Jayanthi!)','2026-09-14 13:40:07.663115',19,17,24);
INSERT INTO "REVIEWS" VALUES(18,5,'Very punctual, caring, and communicative with constant photo updates. Will book again! (Simba Cat was so happy with Anandhi!)','2026-09-14 13:40:07.663115',20,18,25);
INSERT INTO "REVIEWS" VALUES(19,4,'Great sitter, followed all feeding and walking instructions carefully. (Maximus was so happy with Dinesh!)','2026-09-14 13:40:07.671257',21,19,26);
INSERT INTO "REVIEWS" VALUES(20,5,'Outstanding service! Treated my pet like family. Could not ask for better care. (Maya was so happy with Geetha!)','2026-09-14 13:40:07.671257',22,20,27);
INSERT INTO "REVIEWS" VALUES(21,4,'Very knowledgeable and gentle with large energetic dogs. Excellent experience. (Rex was so happy with Naveen!)','2026-09-14 13:40:07.671257',23,21,28);
INSERT INTO "REVIEWS" VALUES(22,5,'Super responsive and attentive to medical schedules. Top-tier caretaker! (Teddy was so happy with Lakshmi!)','2026-09-14 13:40:07.671257',24,22,29);
INSERT INTO "REVIEWS" VALUES(23,5,'My cat adored her! Clean, stress-free environment and regular grooming. (Bruno was so happy with Hariprasad!)','2026-09-14 13:40:07.679391',25,23,10);
INSERT INTO "REVIEWS" VALUES(24,4,'Punctual and reliable for daily walking sessions. Very satisfied. (Milo was so happy with Shalini!)','2026-09-14 13:40:07.679391',26,24,11);
INSERT INTO "REVIEWS" VALUES(25,5,'The best pet sitting experience in Tamil Nadu. 5 stars all the way! (Bella was so happy with Priya!)','2026-09-14 13:40:07.679391',27,5,12);
INSERT INTO "REVIEWS" VALUES(26,4,'Warm and welcoming family environment. Our dog loved the open play yard. (Oliver was so happy with Suresh!)','2026-09-14 13:40:07.687695',28,6,13);
CREATE TABLE "USERS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "role" varchar(20) NOT NULL, "phone" varchar(20) NULL, "address" varchar(255) NULL, "profile_photo" varchar(100) NULL);
INSERT INTO "USERS" VALUES(1,'pbkdf2_sha256$600000$1o3tooiD4QMEiCluQ4x6Ud$yq3WTpTtgeiwsbtY22nJYbnTiV5qy1CSewSfM9PExL0=','2026-10-15 22:43:04.597774',1,'admin','System','Administrator','admin@petcarecompanion.com',1,1,'2026-08-23 07:06:05.997482','ADMIN',NULL,NULL,'');
INSERT INTO "USERS" VALUES(2,'pbkdf2_sha256$600000$ScB8km82vjX47L8Aj97H3U$KA2W1JjZ7EZLDMn6SDDDrYYYsuiu8OBMJNyAGUK+nP0=','2026-10-15 22:46:46.756337',0,'sarah_jenkins','Sarah','Jenkins','sarah.jenkins@example.com',0,1,'2026-08-23 07:06:06.565600','PET_OWNER','+1 (555) 234-5678','Westfield Park, Austin, TX','profiles/ChatGPT_Image_Jul_19_2026_06_53_39_PM.png');
INSERT INTO "USERS" VALUES(3,'pbkdf2_sha256$600000$8KhQaxtkpmDCo3WadPjpaz$e71C9O1hC5YR3FCpQckfcgc8JEh2avwbNgE1qkt+pEU=',NULL,0,'david_miller','David','Miller','david.miller@example.com',0,1,'2026-08-23 07:06:07.099386','PET_OWNER','+1 (555) 876-5432','South Congress, Austin, TX','');
INSERT INTO "USERS" VALUES(4,'pbkdf2_sha256$600000$5B3YMQF8YmekZKxv2dbfXW$7Nt9nOZ4TNfb4r67rWKa4Os3QCqPl5CzmPjYxBIi2Lg=',NULL,0,'priya_sharma','Priya','Sharma','priya.sharma@example.com',0,1,'2026-08-23 07:06:07.601961','PET_OWNER','+1 (555) 432-1098','Downtown, Austin, TX','');
INSERT INTO "USERS" VALUES(5,'pbkdf2_sha256$600000$NK67G6NAKvptFgpXi7GxwF$vaaVsGyKXWuUMhRYYqO0zgs34S8YHlL2v4CNbUyLmbc=',NULL,0,'alex_rivera','Alex','Rivera','alex.rivera@example.com',0,1,'2026-08-23 07:06:08.097676','CARETAKER','+1 (555) 321-7654','Zilker Area, Austin, TX','');
INSERT INTO "USERS" VALUES(6,'pbkdf2_sha256$600000$ZXsSsU2UXMszHENeKCHAc5$y9mgR4o6X2PNQ7mlv9YI7cuuMK7dQikXgbwKLKJuL/A=',NULL,0,'elena_rostova','Elena','Rostova','elena.rostova@example.com',0,1,'2026-08-23 07:06:08.625491','CARETAKER','+1 (555) 901-2345','Hyde Park, Austin, TX','');
INSERT INTO "USERS" VALUES(7,'pbkdf2_sha256$600000$9kg3WDZpKHWzjp4IFBf8f5$kpWtrov4oAOVVS/7MGqr/G07BK1N+AiodBlCRFOld6M=',NULL,0,'marcus_vance','Marcus','Vance','marcus.vance@example.com',0,1,'2026-08-23 07:06:09.161256','CARETAKER','+1 (555) 678-9012','East Riverside, Austin, TX','');
INSERT INTO "USERS" VALUES(8,'pbkdf2_sha256$600000$uzIA34whgHyBQCxF4HbRfg$Ln+wD5nrUceCa03LLtC7UB0qqeasnduX+jp6TEyeDnU=',NULL,0,'chloe_bennett','Chloe','Bennett','chloe.bennett@example.com',0,1,'2026-08-23 07:06:09.672098','CARETAKER','+1 (555) 543-2109','Mueller, Austin, TX','');
INSERT INTO "USERS" VALUES(9,'pbkdf2_sha256$600000$4RPyVPPpEemLrmhULQSCo8$FGZV9jwkMkEGEeXLWmQbMqYXB/xwkcQLK/Cb1Jr7G4A=','2026-10-09 05:20:21.729051',0,'john','','','',0,1,'2026-09-14 13:02:54.482586','PET_OWNER',NULL,'madurai','');
INSERT INTO "USERS" VALUES(10,'pbkdf2_sha256$600000$s5lZHW3prFGny9ZRygo8aP$uxmzzWscFkGe/cZwIXaNn76r611aMqsgtOHI6l54CF8=','2026-10-18 11:30:05.321913',0,'customer01','Akash','Kumar','customer01@example.com',0,1,'2026-09-14 13:39:54.798742','PET_OWNER','+91 98401 23401','14, 2nd Avenue, Anna Nagar, Chennai, Tamil Nadu - 600040','customers/customer_01.jpg');
INSERT INTO "USERS" VALUES(11,'pbkdf2_sha256$600000$vYnBIAYwMsre3jCeY2U9WP$HLfBcoVlmeyPypAYbxQggfzRd/sQHljn3UG3FMq50UY=',NULL,0,'customer02','Divya','Krishnan','customer02@example.com',0,1,'2026-09-14 13:39:55.036377','PET_OWNER','+91 98421 34502','28, 80 Feet Road, KK Nagar, Madurai, Tamil Nadu - 625020','customers/customer_02.jpg');
INSERT INTO "USERS" VALUES(12,'pbkdf2_sha256$600000$sgKjnzdvn1bJULVLQfSPwo$P/Y48/ujPvtI1BUHez6JSu8azsUc28URPqOt1Ezcu7Y=',NULL,0,'customer03','Rajesh','Kannan','customer03@example.com',0,1,'2026-09-14 13:39:55.323947','PET_OWNER','+91 98940 45603','45, DB Road, RS Puram, Coimbatore, Tamil Nadu - 641002','customers/customer_03.jpg');
INSERT INTO "USERS" VALUES(13,'pbkdf2_sha256$600000$gL0ko4VTM4zIYwAv2hZuxd$GaZm8QiMQbOnfvmYlT8jDvobg/qArIMPzN0wSpLkCSo=',NULL,0,'customer04','Meenakshi','Sundaram','customer04@example.com',0,1,'2026-09-14 13:39:55.580647','PET_OWNER','+91 94431 56704','9, Main Road, Thillai Nagar, Trichy, Tamil Nadu - 620018','customers/customer_04.jpg');
INSERT INTO "USERS" VALUES(14,'pbkdf2_sha256$600000$78LBowucOtSfhfE7UCiemi$tYDGhyuFDPhO0DT1slGa84PwVT/P1ISgm7CGJdp+akc=',NULL,0,'customer05','Karthik','Rajan','customer05@example.com',0,1,'2026-09-14 13:39:55.846188','PET_OWNER','+91 97890 67805','72, Brindavan Road, Fairlands, Salem, Tamil Nadu - 636016','customers/customer_05.jpg');
INSERT INTO "USERS" VALUES(15,'pbkdf2_sha256$600000$16ZxGIHI4L4it8O70q1RDL$Yp8BZEqiSZ2oK3SXvI+Sly8ht/BX4qP9GwBhPod4zso=',NULL,0,'customer06','Ananya','Swaminathan','customer06@example.com',0,1,'2026-09-14 13:39:56.141734','PET_OWNER','+91 96290 78906','19, South Bye Pass Road, Palayamkottai, Tirunelveli, Tamil Nadu - 627002','customers/customer_06.jpg');
INSERT INTO "USERS" VALUES(16,'pbkdf2_sha256$600000$zvCOOyls8TBU3HG5TrOwMp$/kzcLbji6sMTv92wCxx8l4eIDxQn7ReWc2tbhqtRpg0=',NULL,0,'customer07','Vigneshwaran','Balan','customer07@example.com',0,1,'2026-09-14 13:39:56.416407','PET_OWNER','+91 99440 89007','55, Srivilliputhur Road, Satchiyapuram, Sivakasi, Tamil Nadu - 626124','customers/customer_07.jpg');
INSERT INTO "USERS" VALUES(17,'pbkdf2_sha256$600000$kwmi2Q9yX3MNTLA8LY6XAy$GTAqmYxfQJNQV/6/iq/erClAiemcKsksCwBBs1ATgWY=',NULL,0,'customer08','Shalini','Natarajan','customer08@example.com',0,1,'2026-09-14 13:39:56.714355','PET_OWNER','+91 98430 90108','31, GTN Salai, Dindigul, Tamil Nadu - 624005','customers/customer_08.jpg');
INSERT INTO "USERS" VALUES(18,'pbkdf2_sha256$600000$I8fB0HVP8VJstLWvLsU8pA$6LR8hS2J4lv9vtJSaYTppap/wXxJmhzlaeUkcg+u36Q=',NULL,0,'customer09','Praveen','Chandran','customer09@example.com',0,1,'2026-09-14 13:39:56.991851','PET_OWNER','+91 94420 01209','84, Medical College Road, Thanjavur, Tamil Nadu - 613004','customers/customer_09.jpg');
INSERT INTO "USERS" VALUES(19,'pbkdf2_sha256$600000$fzXY4NhRnPzNHTPZ3HPo3i$fvdKNEdNH91sX6ZuOVd9Nq78ss3BsSXCwnipYPdfUe8=',NULL,0,'customer10','Kavitha','Murugan','customer10@example.com',0,1,'2026-09-14 13:39:57.275054','PET_OWNER','+91 98427 12310','112, Perundurai Road, Erode, Tamil Nadu - 638011','customers/customer_10.jpg');
INSERT INTO "USERS" VALUES(20,'pbkdf2_sha256$600000$hXbnVnDAatFKG0eP9ywVLE$+RhQmPiS+rdVON2Efd0D6HHwPjIZ7RD97+f8AlLmgo4=',NULL,0,'customer11','Senthil','Nathan','customer11@example.com',0,1,'2026-09-14 13:39:57.542481','PET_OWNER','+91 99940 23411','23, Kumaran Road, Tiruppur, Tamil Nadu - 641601','customers/customer_11.jpg');
INSERT INTO "USERS" VALUES(21,'pbkdf2_sha256$600000$3zdlQG8Y2mimd4q4AP998Z$ontXEb3RyR12vD7pTxUrDBZQvoegMRsq5PK97uABsLU=',NULL,0,'customer12','Deepika','Ramesh','customer12@example.com',0,1,'2026-09-14 13:39:57.843950','PET_OWNER','+91 97870 34512','67, Gandhi Nagar, Katpadi, Vellore, Tamil Nadu - 632014','customers/customer_12.jpg');
INSERT INTO "USERS" VALUES(22,'pbkdf2_sha256$600000$IqNhlIgtr0qHO8lJaFiKhu$2TrdUlUWgnk5+0qzUWNxFVidiJPWIzqclca5lIoyINI=',NULL,0,'customer13','Arunkumar','Veerappan','customer13@example.com',0,1,'2026-09-14 13:39:58.156180','PET_OWNER','+91 94860 45613','10, Court Road, Nagercoil, Tamil Nadu - 629001','customers/customer_13.jpg');
INSERT INTO "USERS" VALUES(23,'pbkdf2_sha256$600000$jWjKFa30lgo2LsQiuvFVA5$9IHgpqLmmYChR3kixWC1Wz8zCHhp2olXArTG23n+bz4=',NULL,0,'customer14','Nithya','Subbiah','customer14@example.com',0,1,'2026-09-14 13:39:58.427329','PET_OWNER','+91 98432 56714','48, Jawahar Bazaar, Karur, Tamil Nadu - 639001','customers/customer_14.jpg');
INSERT INTO "USERS" VALUES(24,'pbkdf2_sha256$600000$afdV0v1DnM1V9v23YwsKBe$kpoe4j6a3dZnh/Oo6ck9mjqLfmJA4sAA/gMFCdIz4ek=',NULL,0,'customer15','Saravanan','Govind','customer15@example.com',0,1,'2026-09-14 13:39:58.693068','PET_OWNER','+91 96000 67815','105, Gandhi Road, Kanchipuram, Tamil Nadu - 631501','customers/customer_15.jpg');
INSERT INTO "USERS" VALUES(25,'pbkdf2_sha256$600000$Wi6WX4sTe3QnT5OiJiQ3on$Sy3Ypl4Rvrmz3Q4DIUbTayCN+1/9WQULFpUV32Avhko=',NULL,0,'customer16','Poornima','Selvam','customer16@example.com',0,1,'2026-09-14 13:39:58.959264','PET_OWNER','+91 98424 78916','18, TSR Big Street, Kumbakonam, Tamil Nadu - 612001','customers/customer_16.jpg');
INSERT INTO "USERS" VALUES(26,'pbkdf2_sha256$600000$I6CU2Xiw3JkaecWDdvXTwe$5AjV4BQlFWUgDUF6/hDXGI2U3BUyT0IxoGKx9GuSv4w=',NULL,0,'customer17','Balaji','Parthiban','customer17@example.com',0,1,'2026-09-14 13:39:59.290648','PET_OWNER','+91 94433 89017','92, Cruz Fernandez Avenue, Millerpuram, Thoothukudi, Tamil Nadu - 628008','customers/customer_17.jpg');
INSERT INTO "USERS" VALUES(27,'pbkdf2_sha256$600000$Ql35oSCWtOLGOOLKUPmQGn$vLmHjEaXyXqlVLUYx57Kc7guSWqijRH4PIqMA2Anit0=',NULL,0,'customer18','Harini','Raman','customer18@example.com',0,1,'2026-09-14 13:39:59.704370','PET_OWNER','+91 97500 90118','34, New Scheme Road, Pollachi, Tamil Nadu - 642001','customers/customer_18.jpg');
INSERT INTO "USERS" VALUES(28,'pbkdf2_sha256$600000$tQpWwPEEaFlLSiExRjzRbR$KmIMoSlmVaYfn1EMpcHjiIT2LvsQsR1MsdCWf7nfV5s=',NULL,0,'customer19','Vijay','Anand','customer19@example.com',0,1,'2026-09-14 13:40:00.020056','PET_OWNER','+91 98945 01219','51, Bagalur Road, Hosur, Tamil Nadu - 635109','customers/customer_19.jpg');
INSERT INTO "USERS" VALUES(29,'pbkdf2_sha256$600000$GiM3aphARRzgpE7EqCLZHg$iXFimgEPhDCYM4Xg99pOAo0TD1leYuoyalcknOFE/pU=',NULL,0,'customer20','Sneha','Manickam','customer20@example.com',0,1,'2026-09-14 13:40:00.332830','PET_OWNER','+91 94437 12320','8, Salai Street, Ramanathapuram, Tamil Nadu - 623501','customers/customer_20.jpg');
INSERT INTO "USERS" VALUES(30,'pbkdf2_sha256$600000$ckhfqiI9nlR7A4QxTgL1Fl$Noa1Taf3jn8wq3RhGnadq9o7A30RiQvLsEuPOLAg818=','2026-09-14 13:53:59.596419',0,'caretaker01','Priya','Sharma','caretaker01@example.com',0,1,'2026-09-14 13:40:00.666561','CARETAKER','+91 98421 99001','42, West Veli Street, Madurai, Tamil Nadu - 625001','caretakers/caretaker_01.jpg');
INSERT INTO "USERS" VALUES(31,'pbkdf2_sha256$600000$oHsquwrS4eEnIRrR047sr3$caGaAkGSgIn1g1yhlbLyqmOf2OTzcv8XNjy8Jdwdg4Y=',NULL,0,'caretaker02','Suresh','Kumar','caretaker02@example.com',0,1,'2026-09-14 13:40:00.997775','CARETAKER','+91 98402 99002','15, GST Road, Guindy, Chennai, Tamil Nadu - 600032','caretakers/caretaker_02.jpg');
INSERT INTO "USERS" VALUES(32,'pbkdf2_sha256$600000$uGQYbpbCrTp7QNagmrocPi$dLcT4JCzwMUOZIpwjkMEimDq/bTD7f1k2iFUUEagVqg=','2026-10-18 10:38:35.360993',0,'caretaker03','Karthikeyan','Murugan','caretaker03@example.com',0,1,'2026-09-14 13:40:01.337129','CARETAKER','+91 98941 99003','88, Avinashi Road, Peelamedu, Coimbatore, Tamil Nadu - 641004','caretakers/caretaker_03.jpg');
INSERT INTO "USERS" VALUES(33,'pbkdf2_sha256$600000$lTCVY3LCQqSthg7yoMpA5Y$UoRX4lAcSxb15OojKkApf+/ZK5XRnGHbIUAIl2CZVZk=',NULL,0,'caretaker04','Deepa','Balaji','caretaker04@example.com',0,1,'2026-09-14 13:40:01.643692','CARETAKER','+91 94432 99004','22, Cantonment, Trichy, Tamil Nadu - 620001','caretakers/caretaker_04.jpg');
INSERT INTO "USERS" VALUES(34,'pbkdf2_sha256$600000$gSnFEOSSdZjivmkb3kevDI$FdHBBBxJLGDuVspM4H0HfOVEFpeyjcjjgYdKtOnVoks=',NULL,0,'caretaker05','Ramesh','Varma','caretaker05@example.com',0,1,'2026-09-14 13:40:01.939048','CARETAKER','+91 97891 99005','34, Omalur Main Road, Salem, Tamil Nadu - 636009','caretakers/caretaker_05.jpg');
INSERT INTO "USERS" VALUES(35,'pbkdf2_sha256$600000$zkCk3IW1tnOT0SPLXyFDqa$e1Rnu1+Zb69o3HryBOLAdYnd42toUjx53GT9TYNcvHU=',NULL,0,'caretaker06','Preethi','Sundar','caretaker06@example.com',0,1,'2026-09-14 13:40:02.241878','CARETAKER','+91 96291 99006','51, Trivandrum Road, Tirunelveli, Tamil Nadu - 627003','caretakers/caretaker_06.jpg');
INSERT INTO "USERS" VALUES(36,'pbkdf2_sha256$600000$ktWP57chEQmLtV5hxjLfhV$e9UGPjrJHXP3Z58De1ht2y9tQqBR5qSgX7YpeFF2RI0=',NULL,0,'caretaker07','Manikandan','Raman','caretaker07@example.com',0,1,'2026-09-14 13:40:02.494243','CARETAKER','+91 99441 99007','77, Chairman Shanmugam Road, Sivakasi, Tamil Nadu - 626123','caretakers/caretaker_07.jpg');
INSERT INTO "USERS" VALUES(37,'pbkdf2_sha256$600000$70lWGKaewJ0V1GxWll3obB$8c1vNWZ7uKe0S+3uE0uq7eJ4JsESOOHkCdohVGm3HeA=',NULL,0,'caretaker08','Gowri','Shankar','caretaker08@example.com',0,1,'2026-09-14 13:40:02.882733','CARETAKER','+91 98431 99008','12, Palani Road, Dindigul, Tamil Nadu - 624001','caretakers/caretaker_08.jpg');
INSERT INTO "USERS" VALUES(38,'pbkdf2_sha256$600000$A4qiguPrsf2oignQJfCvaY$5iVimQ4N4rmFhyyx+/0chVnoCk9Yl5dFkcTzS67oU+c=',NULL,0,'caretaker09','Revathi','Nathan','caretaker09@example.com',0,1,'2026-09-14 13:40:03.265605','CARETAKER','+91 94421 99009','90, South Main Street, Thanjavur, Tamil Nadu - 613009','caretakers/caretaker_09.jpg');
INSERT INTO "USERS" VALUES(39,'pbkdf2_sha256$600000$CN5VR9CYjiXXEH0eI2ekPS$YBeHgIR3Z/37nIG713oPKsXN1qtwXnff4ABjfeYamnQ=',NULL,0,'caretaker10','Ashok','Selvan','caretaker10@example.com',0,1,'2026-09-14 13:40:03.570669','CARETAKER','+91 98428 99010','64, Brough Road, Erode, Tamil Nadu - 638001','caretakers/caretaker_10.jpg');
INSERT INTO "USERS" VALUES(40,'pbkdf2_sha256$600000$SoSlztcGzpKq87zXKPx5pc$fk3TE8LYibm5T3lbYqI+lLaqKg+loDYPC8VDSTcuoZ4=',NULL,0,'caretaker11','Bhuvaneshwari','K','caretaker11@example.com',0,1,'2026-09-14 13:40:03.891428','CARETAKER','+91 99941 99011','38, Kangayam Road, Tiruppur, Tamil Nadu - 641604','caretakers/caretaker_11.jpg');
INSERT INTO "USERS" VALUES(41,'pbkdf2_sha256$600000$BLnle5OqLrW3iixpAzZeMu$XDrnAWkwgQGuqvazWVmUQDSxZyLFu7c6Bf0oqk6ioFw=',NULL,0,'caretaker12','Vignesh','Pandian','caretaker12@example.com',0,1,'2026-09-14 13:40:04.199897','CARETAKER','+91 97871 99012','102, Officer Line, Vellore, Tamil Nadu - 632001','caretakers/caretaker_12.jpg');
INSERT INTO "USERS" VALUES(42,'pbkdf2_sha256$600000$ee8LSPL8Pb5ZsLVLXq7rJz$2ifUjNxsabRZWt2OyA8Rd66gdBhiY9qUKmkqGBL7k4Y=',NULL,0,'caretaker13','Jayanthi','Ramanathan','caretaker13@example.com',0,1,'2026-09-14 13:40:04.490458','CARETAKER','+91 94861 99013','26, Cape Road, Nagercoil, Tamil Nadu - 629002','caretakers/caretaker_13.jpg');
INSERT INTO "USERS" VALUES(43,'pbkdf2_sha256$600000$q5mcL2UgeBXuWh9g1u67Qb$84H8l/45eesO5icXL68GE9UwP6EpS6diLOeaMQUYbo4=','2026-10-18 05:53:56.745709',0,'caretaker14','Anandhi','Muthukumar','caretaker14@example.com',0,1,'2026-09-14 13:40:04.803119','CARETAKER','+91 98433 99014','81, Kovai Road, Karur, Tamil Nadu - 639002','caretakers/caretaker_14.jpg');
INSERT INTO "USERS" VALUES(44,'pbkdf2_sha256$600000$u0HMQdK3PiMElS9eWbPhy3$q/UsWZRaWrMIj3/ht8pZfOywlQdj5xb+nTntAllTQ2k=',NULL,0,'caretaker15','Dinesh','Chandran','caretaker15@example.com',0,1,'2026-09-14 13:40:05.108294','CARETAKER','+91 96001 99015','14, Ekambaranathar Sannathi, Kanchipuram, Tamil Nadu - 631502','caretakers/caretaker_15.jpg');
INSERT INTO "USERS" VALUES(45,'pbkdf2_sha256$600000$R2MCXywLdhtCgAFXyvfFVZ$RVxjAIDkWi2NlnwUiSxFnPpRcn0OXZhGhfEySK9Tru8=',NULL,0,'caretaker16','Geetha','Sridhar','caretaker16@example.com',0,1,'2026-09-14 13:40:05.462961','CARETAKER','+91 98425 99016','55, Kumbeswarar South Street, Kumbakonam, Tamil Nadu - 612001','caretakers/caretaker_16.jpg');
INSERT INTO "USERS" VALUES(46,'pbkdf2_sha256$600000$vCkmHZkW9fp6k3ZqMgehAg$/pIYNHj8rajZQw348id7aCnbudsumHtPyeaTSa6WxEw=',NULL,0,'caretaker17','Naveen','Prasath','caretaker17@example.com',0,1,'2026-09-14 13:40:05.752477','CARETAKER','+91 94434 99017','43, Palayamkottai Road, Thoothukudi, Tamil Nadu - 628003','caretakers/caretaker_17.jpg');
INSERT INTO "USERS" VALUES(47,'pbkdf2_sha256$600000$1nWCfnHeO3njM9Psi2U2ab$Lqx1IKzEXXrq6XycvkHDStUuXUtu8UW39ZOqqzxxpE4=',NULL,0,'caretaker18','Lakshmi','Narayanan','caretaker18@example.com',0,1,'2026-09-14 13:40:05.992784','CARETAKER','+91 97501 99018','60, Meenkarai Road, Pollachi, Tamil Nadu - 642001','caretakers/caretaker_18.jpg');
INSERT INTO "USERS" VALUES(48,'pbkdf2_sha256$600000$gy21DCMidOpmKBgxlwQ9oI$41ffI4fzdHFyYd4FJE70qYprHQWNjx/gKgCIHYAu8U8=',NULL,0,'caretaker19','Hariprasad','Swaminathan','caretaker19@example.com',0,1,'2026-09-14 13:40:06.326937','CARETAKER','+91 98946 99019','118, Denkanikotta Road, Hosur, Tamil Nadu - 635109','caretakers/caretaker_19.jpg');
INSERT INTO "USERS" VALUES(49,'pbkdf2_sha256$600000$XPxWdSzlzyv1V6MppVKEc3$xQ2HHRPoj9rrEwiZhjXMSy7xLe1rewBXcKcRfAmstuA=',NULL,0,'caretaker20','Shalini','Vimal','caretaker20@example.com',0,1,'2026-09-14 13:40:06.613977','CARETAKER','+91 94438 99020','29, Vandikkara Street, Ramanathapuram, Tamil Nadu - 623501','caretakers/caretaker_20.jpg');
INSERT INTO "USERS" VALUES(50,'pbkdf2_sha256$600000$oKDPbTnvepxjVSLevHoZ6m$p7hwT5d8/1S1kfacoF5ykX471zWtOft0raWDaL4rW3U=',NULL,0,'gopika','gopi','M','g@gmail.com',0,1,'2026-10-15 22:37:24.780971','PET_OWNER','1234567889','Madurai','');
INSERT INTO "USERS" VALUES(51,'pbkdf2_sha256$600000$K8sI7ZEFfSg5GLAceNuFFZ$vFtSYkF3AGM043zc1Hs6DOR0L9XUz6buszYPD02QyNA=',NULL,0,'testowner99','Test','Owner','testowner99@example.com',0,1,'2026-10-15 22:41:08.555338','PET_OWNER',NULL,NULL,'');
INSERT INTO "USERS" VALUES(54,'pbkdf2_sha256$600000$XyvvGVJp57b22SbKT7Hpj9$Hqjw38+Vd0WpIMMqV/MvjYrdewoV34hgkhy/ORxpctk=','2026-10-15 22:52:45.630171',0,'aathi','aathi','N','a@gmail.ocm',0,1,'2026-10-15 22:52:45.112966','PET_OWNER','1593478628','Madurai','');
INSERT INTO "USERS" VALUES(55,'',NULL,0,'paws_shelter','PAWS','Animal Rescue','contact@pawsindia.org',0,1,'2026-10-15 22:57:40.563149','PET_OWNER','+91 98401 22334','Besant Nagar, Chennai','');
CREATE TABLE "USERS_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "USERS_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "VACCINATIONS" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "vaccine_name" varchar(150) NOT NULL, "administered_date" date NOT NULL, "next_due_date" date NOT NULL, "batch_number" varchar(50) NULL, "vet_name" varchar(150) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "VACCINATIONS" VALUES(1,'Rabies 3-Year Booster','2025-10-27','2028-10-26','RAB-9923','Dr. Emily Watson (Austin Animal Care)','2026-08-23 07:06:10.520588',1);
INSERT INTO "VACCINATIONS" VALUES(2,'DHPP Core Vaccine','2025-09-07','2026-09-07','DHPP-5401','Dr. Emily Watson','2026-08-23 07:06:10.529891',1);
INSERT INTO "VACCINATIONS" VALUES(3,'Bordetella Kennel Cough','2026-02-14','2026-08-13','BORD-1122','Dr. Robert Hayes','2026-08-23 07:06:10.537777',3);
INSERT INTO "VACCINATIONS" VALUES(4,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.707245',5);
INSERT INTO "VACCINATIONS" VALUES(5,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.708318',5);
INSERT INTO "VACCINATIONS" VALUES(6,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.709490',5);
INSERT INTO "VACCINATIONS" VALUES(7,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.713962',6);
INSERT INTO "VACCINATIONS" VALUES(8,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.714595',6);
INSERT INTO "VACCINATIONS" VALUES(9,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.718434',7);
INSERT INTO "VACCINATIONS" VALUES(10,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.720528',8);
INSERT INTO "VACCINATIONS" VALUES(11,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.720528',8);
INSERT INTO "VACCINATIONS" VALUES(12,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.720528',8);
INSERT INTO "VACCINATIONS" VALUES(13,'FVRCP 3-in-1 Feline Core','2026-02-16','2026-09-18','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.728968',9);
INSERT INTO "VACCINATIONS" VALUES(14,'Feline Rabies Vaccine','2025-10-29','2026-09-18','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.728968',9);
INSERT INTO "VACCINATIONS" VALUES(15,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.728968',10);
INSERT INTO "VACCINATIONS" VALUES(16,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.728968',10);
INSERT INTO "VACCINATIONS" VALUES(17,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.740829',10);
INSERT INTO "VACCINATIONS" VALUES(18,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.749931',11);
INSERT INTO "VACCINATIONS" VALUES(19,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.749931',11);
INSERT INTO "VACCINATIONS" VALUES(20,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.753498',11);
INSERT INTO "VACCINATIONS" VALUES(21,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.769718',12);
INSERT INTO "VACCINATIONS" VALUES(22,'Rabies (Annual Booster)','2026-03-18','2026-08-30','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.769718',13);
INSERT INTO "VACCINATIONS" VALUES(23,'DHPP 5-in-1 Core Vaccine','2026-01-17','2026-08-30','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.769718',13);
INSERT INTO "VACCINATIONS" VALUES(24,'Bordetella (Kennel Cough)','2025-11-18','2026-08-30','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.777951',13);
INSERT INTO "VACCINATIONS" VALUES(25,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.778433',14);
INSERT INTO "VACCINATIONS" VALUES(26,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.786070',14);
INSERT INTO "VACCINATIONS" VALUES(27,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.786070',15);
INSERT INTO "VACCINATIONS" VALUES(28,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.786070',15);
INSERT INTO "VACCINATIONS" VALUES(29,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.786070',15);
INSERT INTO "VACCINATIONS" VALUES(30,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.794251',16);
INSERT INTO "VACCINATIONS" VALUES(31,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.794251',16);
INSERT INTO "VACCINATIONS" VALUES(32,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.794251',17);
INSERT INTO "VACCINATIONS" VALUES(33,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.802659',18);
INSERT INTO "VACCINATIONS" VALUES(34,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.802659',18);
INSERT INTO "VACCINATIONS" VALUES(35,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.802659',18);
INSERT INTO "VACCINATIONS" VALUES(36,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.802659',19);
INSERT INTO "VACCINATIONS" VALUES(37,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.802659',19);
INSERT INTO "VACCINATIONS" VALUES(38,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.810788',20);
INSERT INTO "VACCINATIONS" VALUES(39,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.810788',20);
INSERT INTO "VACCINATIONS" VALUES(40,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.810788',20);
INSERT INTO "VACCINATIONS" VALUES(41,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.810788',21);
INSERT INTO "VACCINATIONS" VALUES(42,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.810788',21);
INSERT INTO "VACCINATIONS" VALUES(43,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.810788',21);
INSERT INTO "VACCINATIONS" VALUES(44,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.819166',22);
INSERT INTO "VACCINATIONS" VALUES(45,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.819166',22);
INSERT INTO "VACCINATIONS" VALUES(46,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.819166',23);
INSERT INTO "VACCINATIONS" VALUES(47,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.827719',24);
INSERT INTO "VACCINATIONS" VALUES(48,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.827719',24);
INSERT INTO "VACCINATIONS" VALUES(49,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.827719',24);
INSERT INTO "VACCINATIONS" VALUES(50,'FVRCP 3-in-1 Feline Core','2026-02-16','2026-09-18','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.827719',25);
INSERT INTO "VACCINATIONS" VALUES(51,'Feline Rabies Vaccine','2025-10-29','2026-09-18','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.836113',25);
INSERT INTO "VACCINATIONS" VALUES(52,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.838053',26);
INSERT INTO "VACCINATIONS" VALUES(53,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.842916',27);
INSERT INTO "VACCINATIONS" VALUES(54,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.844424',27);
INSERT INTO "VACCINATIONS" VALUES(55,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.844762',27);
INSERT INTO "VACCINATIONS" VALUES(56,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.844762',28);
INSERT INTO "VACCINATIONS" VALUES(57,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.844762',28);
INSERT INTO "VACCINATIONS" VALUES(58,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.844762',29);
INSERT INTO "VACCINATIONS" VALUES(59,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.852895',29);
INSERT INTO "VACCINATIONS" VALUES(60,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.853404',29);
INSERT INTO "VACCINATIONS" VALUES(61,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.856667',30);
INSERT INTO "VACCINATIONS" VALUES(62,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.856667',30);
INSERT INTO "VACCINATIONS" VALUES(63,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.856667',30);
INSERT INTO "VACCINATIONS" VALUES(64,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.863541',31);
INSERT INTO "VACCINATIONS" VALUES(65,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.864699',31);
INSERT INTO "VACCINATIONS" VALUES(66,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.866981',32);
INSERT INTO "VACCINATIONS" VALUES(67,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.869902',33);
INSERT INTO "VACCINATIONS" VALUES(68,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.874496',33);
INSERT INTO "VACCINATIONS" VALUES(69,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.874496',33);
INSERT INTO "VACCINATIONS" VALUES(70,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.877929',34);
INSERT INTO "VACCINATIONS" VALUES(71,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.877929',34);
INSERT INTO "VACCINATIONS" VALUES(72,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.877929',34);
INSERT INTO "VACCINATIONS" VALUES(73,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.877929',35);
INSERT INTO "VACCINATIONS" VALUES(74,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.891149',36);
INSERT INTO "VACCINATIONS" VALUES(75,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.891149',36);
INSERT INTO "VACCINATIONS" VALUES(76,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.895835',37);
INSERT INTO "VACCINATIONS" VALUES(77,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.895835',37);
INSERT INTO "VACCINATIONS" VALUES(78,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.903357',38);
INSERT INTO "VACCINATIONS" VALUES(79,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.903357',38);
INSERT INTO "VACCINATIONS" VALUES(80,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.903357',38);
INSERT INTO "VACCINATIONS" VALUES(81,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.910824',39);
INSERT INTO "VACCINATIONS" VALUES(82,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.910824',39);
INSERT INTO "VACCINATIONS" VALUES(83,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.910824',39);
INSERT INTO "VACCINATIONS" VALUES(84,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.919206',40);
INSERT INTO "VACCINATIONS" VALUES(85,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.919206',40);
INSERT INTO "VACCINATIONS" VALUES(86,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.928137',41);
INSERT INTO "VACCINATIONS" VALUES(87,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.936275',42);
INSERT INTO "VACCINATIONS" VALUES(88,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.936275',42);
INSERT INTO "VACCINATIONS" VALUES(89,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.936275',42);
INSERT INTO "VACCINATIONS" VALUES(90,'Rabies (Annual Booster)','2026-03-18','2026-09-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.944756',43);
INSERT INTO "VACCINATIONS" VALUES(91,'DHPP 5-in-1 Core Vaccine','2026-01-17','2026-09-18','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.944756',43);
INSERT INTO "VACCINATIONS" VALUES(92,'Bordetella (Kennel Cough)','2025-11-18','2026-09-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.944756',43);
INSERT INTO "VACCINATIONS" VALUES(93,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.953577',44);
INSERT INTO "VACCINATIONS" VALUES(94,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.957617',45);
INSERT INTO "VACCINATIONS" VALUES(95,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.961397',45);
INSERT INTO "VACCINATIONS" VALUES(96,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.961397',45);
INSERT INTO "VACCINATIONS" VALUES(97,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.961397',46);
INSERT INTO "VACCINATIONS" VALUES(98,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.961397',46);
INSERT INTO "VACCINATIONS" VALUES(99,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.970660',47);
INSERT INTO "VACCINATIONS" VALUES(100,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.971844',47);
INSERT INTO "VACCINATIONS" VALUES(101,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.971844',47);
INSERT INTO "VACCINATIONS" VALUES(102,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.976236',48);
INSERT INTO "VACCINATIONS" VALUES(103,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.976236',48);
INSERT INTO "VACCINATIONS" VALUES(104,'Rabies (Annual Booster)','2026-03-18','2027-03-18','BATCH-RB-9921','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.977984',49);
INSERT INTO "VACCINATIONS" VALUES(105,'DHPP 5-in-1 Core Vaccine','2026-01-17','2027-01-17','BATCH-DH-4410','Dr. V. Arulraj BVSc','2026-09-14 13:40:07.977984',49);
INSERT INTO "VACCINATIONS" VALUES(106,'Bordetella (Kennel Cough)','2025-11-18','2026-11-18','BATCH-BD-1123','Dr. K. Jayanthi BVSc','2026-09-14 13:40:07.977984',49);
INSERT INTO "VACCINATIONS" VALUES(107,'FVRCP 3-in-1 Feline Core','2026-02-16','2027-02-16','BATCH-FV-3321','Dr. R. Meena BVSc','2026-09-14 13:40:07.986452',50);
INSERT INTO "VACCINATIONS" VALUES(108,'Feline Rabies Vaccine','2025-10-29','2026-10-29','BATCH-FR-8812','Dr. S. Sundaram BVSc','2026-09-14 13:40:07.986452',50);
INSERT INTO "VACCINATIONS" VALUES(109,'Exotic Companion Health Booster','2026-04-17','2027-04-17','BATCH-EX-1011','Dr. M. Deepan BVSc','2026-09-14 13:40:07.994276',51);
CREATE TABLE "WEIGHT_HISTORY" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "recorded_date" date NOT NULL, "weight_kg" decimal NOT NULL, "notes" varchar(255) NULL, "created_at" datetime NOT NULL, "pet_id" bigint NOT NULL REFERENCES "PETS" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "WEIGHT_HISTORY" VALUES(100,'2025-11-04',11.2,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(101,'2026-01-06',10.6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(102,'2026-03-05',10.5,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(103,'2026-05-06',10.1,'Routine checkup & diet evaluation','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(104,'2026-07-06',10.3,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(105,'2026-09-03',9.7,'Pre-seasonal wellness examination','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(106,'2026-10-01',11,'Current logged weight','2026-10-02 00:33:40.603615',53);
INSERT INTO "WEIGHT_HISTORY" VALUES(107,'2025-11-08',28.7,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(108,'2026-01-04',29.3,'Quarterly weight & body condition score check','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(109,'2026-03-09',30.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(110,'2026-05-08',27.9,'Routine checkup & diet evaluation','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(111,'2026-07-04',28.7,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(112,'2026-09-05',29.7,'Pre-seasonal wellness examination','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(113,'2026-09-30',29,'Current logged weight','2026-10-02 00:33:40.609774',52);
INSERT INTO "WEIGHT_HISTORY" VALUES(114,'2025-11-08',0.38,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(115,'2026-01-03',0.4,'Quarterly weight & body condition score check','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(116,'2026-03-07',0.42,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(117,'2026-05-05',0.39,'Routine checkup & diet evaluation','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(118,'2026-07-05',0.4,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(119,'2026-09-03',0.41,'Pre-seasonal wellness examination','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(120,'2026-09-29',0.4,'Current logged weight','2026-10-02 00:33:40.617652',51);
INSERT INTO "WEIGHT_HISTORY" VALUES(121,'2025-11-04',3.55,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(122,'2026-01-04',3.43,'Quarterly weight & body condition score check','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(123,'2026-03-03',3.43,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(124,'2026-05-04',3.28,'Routine checkup & diet evaluation','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(125,'2026-07-03',3.28,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(126,'2026-09-02',3.17,'Pre-seasonal wellness examination','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(127,'2026-10-02',3.5,'Current logged weight','2026-10-02 00:33:40.625905',50);
INSERT INTO "WEIGHT_HISTORY" VALUES(128,'2025-11-06',7,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(129,'2026-01-07',6.9,'Quarterly weight & body condition score check','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(130,'2026-03-09',6.6,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(131,'2026-05-02',6.5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(132,'2026-07-05',6.4,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(133,'2026-09-02',6.4,'Pre-seasonal wellness examination','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(134,'2026-10-04',7,'Current logged weight','2026-10-02 00:33:40.633455',49);
INSERT INTO "WEIGHT_HISTORY" VALUES(135,'2025-11-09',5.9,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(136,'2026-01-04',6.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(137,'2026-03-04',6.3,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(138,'2026-05-05',5.7,'Routine checkup & diet evaluation','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(139,'2026-07-07',6,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(140,'2026-09-04',6.2,'Pre-seasonal wellness examination','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(141,'2026-10-02',6,'Current logged weight','2026-10-02 00:33:40.639721',48);
INSERT INTO "WEIGHT_HISTORY" VALUES(142,'2025-11-06',34.7,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(143,'2026-01-08',34.8,'Quarterly weight & body condition score check','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(144,'2026-03-05',36.5,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(145,'2026-05-03',34,'Routine checkup & diet evaluation','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(146,'2026-07-07',35.2,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(147,'2026-09-04',36.3,'Pre-seasonal wellness examination','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(148,'2026-10-02',35.5,'Current logged weight','2026-10-02 00:33:40.648324',47);
INSERT INTO "WEIGHT_HISTORY" VALUES(149,'2025-11-05',3.85,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(150,'2026-01-04',3.97,'Quarterly weight & body condition score check','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(151,'2026-03-03',3.97,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(152,'2026-05-05',3.84,'Routine checkup & diet evaluation','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(153,'2026-07-02',3.84,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(154,'2026-09-04',4.09,'Pre-seasonal wellness examination','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(155,'2026-10-05',3.9,'Current logged weight','2026-10-02 00:33:40.655216',46);
INSERT INTO "WEIGHT_HISTORY" VALUES(156,'2025-11-05',16.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(157,'2026-01-06',16.4,'Quarterly weight & body condition score check','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(158,'2026-03-09',15.8,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(159,'2026-05-06',15.5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(160,'2026-07-03',15.3,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(161,'2026-09-03',15,'Pre-seasonal wellness examination','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(162,'2026-09-29',16.5,'Current logged weight','2026-10-02 00:33:40.664562',45);
INSERT INTO "WEIGHT_HISTORY" VALUES(163,'2025-11-06',4.86,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(164,'2026-01-06',4.62,'Quarterly weight & body condition score check','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(165,'2026-03-08',4.66,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(166,'2026-05-06',4.53,'Routine checkup & diet evaluation','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(167,'2026-07-02',4.48,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(168,'2026-08-30',4.37,'Pre-seasonal wellness examination','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(169,'2026-10-04',4.8,'Current logged weight','2026-10-02 00:33:40.670555',44);
INSERT INTO "WEIGHT_HISTORY" VALUES(170,'2025-11-08',11.5,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(171,'2026-01-05',11.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(172,'2026-03-08',11.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(173,'2026-05-04',10.7,'Routine checkup & diet evaluation','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(174,'2026-07-07',10.5,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(175,'2026-09-05',10.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(176,'2026-09-29',11.5,'Current logged weight','2026-10-02 00:33:40.679806',43);
INSERT INTO "WEIGHT_HISTORY" VALUES(177,'2025-11-09',29.6,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(178,'2026-01-02',30.5,'Quarterly weight & body condition score check','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(179,'2026-03-06',31.8,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(180,'2026-05-07',29.8,'Routine checkup & diet evaluation','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(181,'2026-07-03',31.3,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(182,'2026-09-04',31.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(183,'2026-10-01',31,'Current logged weight','2026-10-02 00:33:40.687515',42);
INSERT INTO "WEIGHT_HISTORY" VALUES(184,'2025-11-06',0.12,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(185,'2026-01-03',0.12,'Quarterly weight & body condition score check','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(186,'2026-03-08',0.12,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(187,'2026-05-08',0.11,'Routine checkup & diet evaluation','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(188,'2026-07-04',0.11,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(189,'2026-08-31',0.11,'Pre-seasonal wellness examination','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(190,'2026-10-04',0.12,'Current logged weight','2026-10-02 00:33:40.697011',41);
INSERT INTO "WEIGHT_HISTORY" VALUES(191,'2025-11-06',5.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(192,'2026-01-05',5.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(193,'2026-03-03',5,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(194,'2026-05-05',5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(195,'2026-07-06',4.8,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(196,'2026-09-05',4.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(197,'2026-10-05',5.2,'Current logged weight','2026-10-02 00:33:40.704668',40);
INSERT INTO "WEIGHT_HISTORY" VALUES(198,'2025-11-09',7.1,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(199,'2026-01-04',7,'Quarterly weight & body condition score check','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(200,'2026-03-06',7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(201,'2026-05-02',6.7,'Routine checkup & diet evaluation','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(202,'2026-07-03',6.7,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(203,'2026-09-05',6.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(204,'2026-10-01',7.2,'Current logged weight','2026-10-02 00:33:40.715416',39);
INSERT INTO "WEIGHT_HISTORY" VALUES(205,'2025-11-09',35.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(206,'2026-01-06',36.4,'Quarterly weight & body condition score check','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(207,'2026-03-09',36.7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(208,'2026-05-08',35,'Routine checkup & diet evaluation','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(209,'2026-07-07',36.2,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(210,'2026-08-30',37.1,'Pre-seasonal wellness examination','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(211,'2026-10-01',36,'Current logged weight','2026-10-02 00:33:40.723443',38);
INSERT INTO "WEIGHT_HISTORY" VALUES(212,'2025-11-06',3.84,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(213,'2026-01-07',3.88,'Quarterly weight & body condition score check','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(214,'2026-03-08',3.76,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(215,'2026-05-04',3.74,'Routine checkup & diet evaluation','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(216,'2026-07-07',3.62,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(217,'2026-09-04',3.47,'Pre-seasonal wellness examination','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(218,'2026-09-30',3.9,'Current logged weight','2026-10-02 00:33:40.731580',37);
INSERT INTO "WEIGHT_HISTORY" VALUES(219,'2025-11-04',3.44,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(220,'2026-01-04',3.63,'Quarterly weight & body condition score check','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(221,'2026-03-07',3.64,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(222,'2026-05-06',3.54,'Routine checkup & diet evaluation','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(223,'2026-07-06',3.62,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(224,'2026-09-02',3.77,'Pre-seasonal wellness examination','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(225,'2026-09-30',3.6,'Current logged weight','2026-10-02 00:33:40.737482',36);
INSERT INTO "WEIGHT_HISTORY" VALUES(226,'2025-11-07',2.51,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(227,'2026-01-08',2.48,'Quarterly weight & body condition score check','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(228,'2026-03-03',2.35,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(229,'2026-05-05',2.32,'Routine checkup & diet evaluation','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(230,'2026-07-03',2.3,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(231,'2026-08-31',2.25,'Pre-seasonal wellness examination','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(232,'2026-10-02',2.5,'Current logged weight','2026-10-02 00:33:40.745855',35);
INSERT INTO "WEIGHT_HISTORY" VALUES(233,'2025-11-09',51,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(234,'2026-01-07',52.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(235,'2026-03-05',54.4,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(236,'2026-05-07',49.6,'Routine checkup & diet evaluation','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(237,'2026-07-07',51.7,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(238,'2026-08-30',53.3,'Pre-seasonal wellness examination','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(239,'2026-10-05',52,'Current logged weight','2026-10-02 00:33:40.752359',34);
INSERT INTO "WEIGHT_HISTORY" VALUES(240,'2025-11-07',23.5,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.759541',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(241,'2026-01-08',23.6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(242,'2026-03-06',24.6,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(243,'2026-05-02',23.4,'Routine checkup & diet evaluation','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(244,'2026-07-06',23.9,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(245,'2026-09-03',24.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(246,'2026-10-03',24,'Current logged weight','2026-10-02 00:33:40.760549',33);
INSERT INTO "WEIGHT_HISTORY" VALUES(247,'2025-11-06',0.1,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(248,'2026-01-05',0.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(249,'2026-03-03',0.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(250,'2026-05-06',0.1,'Routine checkup & diet evaluation','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(251,'2026-07-07',0.1,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(252,'2026-09-04',0.1,'Pre-seasonal wellness examination','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(253,'2026-10-01',0.04,'Current logged weight','2026-10-02 00:33:40.766785',32);
INSERT INTO "WEIGHT_HISTORY" VALUES(254,'2025-11-08',4.47,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(255,'2026-01-05',4.35,'Quarterly weight & body condition score check','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(256,'2026-03-04',4.38,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(257,'2026-05-02',4.2,'Routine checkup & diet evaluation','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(258,'2026-07-01',4.16,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(259,'2026-08-30',4.13,'Pre-seasonal wellness examination','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(260,'2026-09-30',4.5,'Current logged weight','2026-10-02 00:33:40.773298',31);
INSERT INTO "WEIGHT_HISTORY" VALUES(261,'2025-11-05',7.8,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(262,'2026-01-02',8,'Quarterly weight & body condition score check','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(263,'2026-03-03',8.4,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(264,'2026-05-08',7.8,'Routine checkup & diet evaluation','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(265,'2026-07-06',8.1,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(266,'2026-09-05',8.4,'Pre-seasonal wellness examination','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(267,'2026-10-01',8,'Current logged weight','2026-10-02 00:33:40.781158',30);
INSERT INTO "WEIGHT_HISTORY" VALUES(268,'2025-11-06',30,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(269,'2026-01-04',30.8,'Quarterly weight & body condition score check','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(270,'2026-03-09',31.6,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(271,'2026-05-08',29.9,'Routine checkup & diet evaluation','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(272,'2026-07-07',30.9,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(273,'2026-09-05',31.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(274,'2026-10-04',30.5,'Current logged weight','2026-10-02 00:33:40.787836',29);
INSERT INTO "WEIGHT_HISTORY" VALUES(275,'2025-11-04',3.9,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(276,'2026-01-03',4.15,'Quarterly weight & body condition score check','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(277,'2026-03-07',4.18,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(278,'2026-05-05',4.05,'Routine checkup & diet evaluation','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(279,'2026-07-05',4.08,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(280,'2026-09-03',4.18,'Pre-seasonal wellness examination','2026-10-02 00:33:40.797551',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(281,'2026-10-05',4.1,'Current logged weight','2026-10-02 00:33:40.798542',28);
INSERT INTO "WEIGHT_HISTORY" VALUES(282,'2025-11-06',4.34,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(283,'2026-01-08',4.54,'Quarterly weight & body condition score check','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(284,'2026-03-08',4.69,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(285,'2026-05-07',4.28,'Routine checkup & diet evaluation','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(286,'2026-07-01',4.48,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(287,'2026-09-03',4.71,'Pre-seasonal wellness examination','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(288,'2026-10-05',4.5,'Current logged weight','2026-10-02 00:33:40.804271',27);
INSERT INTO "WEIGHT_HISTORY" VALUES(289,'2025-11-04',1.22,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(290,'2026-01-04',1.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(291,'2026-03-07',1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(292,'2026-05-04',0.94,'Routine checkup & diet evaluation','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(293,'2026-07-05',0.81,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(294,'2026-08-31',0.77,'Pre-seasonal wellness examination','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(295,'2026-10-05',1.2,'Current logged weight','2026-10-02 00:33:40.814280',26);
INSERT INTO "WEIGHT_HISTORY" VALUES(296,'2025-11-05',4.79,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(297,'2026-01-07',4.68,'Quarterly weight & body condition score check','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(298,'2026-03-04',4.61,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(299,'2026-05-04',4.45,'Routine checkup & diet evaluation','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(300,'2026-07-06',4.43,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(301,'2026-08-30',4.33,'Pre-seasonal wellness examination','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(302,'2026-09-29',4.8,'Current logged weight','2026-10-02 00:33:40.820570',25);
INSERT INTO "WEIGHT_HISTORY" VALUES(303,'2025-11-07',12.9,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(304,'2026-01-05',13.3,'Quarterly weight & body condition score check','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(305,'2026-03-08',13.7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(306,'2026-05-02',12.9,'Routine checkup & diet evaluation','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(307,'2026-07-02',13.6,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(308,'2026-09-02',14,'Pre-seasonal wellness examination','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(309,'2026-10-05',13.5,'Current logged weight','2026-10-02 00:33:40.828786',24);
INSERT INTO "WEIGHT_HISTORY" VALUES(310,'2025-11-04',0.1,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(311,'2026-01-05',0.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(312,'2026-03-04',0.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(313,'2026-05-06',0.1,'Routine checkup & diet evaluation','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(314,'2026-07-02',0.1,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(315,'2026-09-03',0.1,'Pre-seasonal wellness examination','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(316,'2026-10-01',0.05,'Current logged weight','2026-10-02 00:33:40.836302',23);
INSERT INTO "WEIGHT_HISTORY" VALUES(317,'2025-11-09',3.94,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(318,'2026-01-02',3.95,'Quarterly weight & body condition score check','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(319,'2026-03-03',4.07,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(320,'2026-05-06',3.83,'Routine checkup & diet evaluation','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(321,'2026-07-05',4.07,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(322,'2026-09-04',4.16,'Pre-seasonal wellness examination','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(323,'2026-09-30',4,'Current logged weight','2026-10-02 00:33:40.844206',22);
INSERT INTO "WEIGHT_HISTORY" VALUES(324,'2025-11-05',19.4,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(325,'2026-01-06',18.9,'Quarterly weight & body condition score check','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(326,'2026-03-06',19,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(327,'2026-05-05',18.5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(328,'2026-07-04',17.8,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(329,'2026-09-03',17.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(330,'2026-10-05',19.5,'Current logged weight','2026-10-02 00:33:40.851181',21);
INSERT INTO "WEIGHT_HISTORY" VALUES(331,'2025-11-06',41.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(332,'2026-01-04',42.3,'Quarterly weight & body condition score check','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(333,'2026-03-05',43.4,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(334,'2026-05-08',41.5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(335,'2026-07-03',41.2,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(336,'2026-08-31',43.2,'Pre-seasonal wellness examination','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(337,'2026-10-04',42,'Current logged weight','2026-10-02 00:33:40.858657',20);
INSERT INTO "WEIGHT_HISTORY" VALUES(338,'2025-11-06',3.12,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(339,'2026-01-07',3.03,'Quarterly weight & body condition score check','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(340,'2026-03-04',2.66,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(341,'2026-05-04',2.45,'Routine checkup & diet evaluation','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(342,'2026-07-03',2.19,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(343,'2026-09-02',2.07,'Pre-seasonal wellness examination','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(344,'2026-10-03',3.2,'Current logged weight','2026-10-02 00:33:40.866095',19);
INSERT INTO "WEIGHT_HISTORY" VALUES(345,'2025-11-03',6.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.870028',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(346,'2026-01-05',6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(347,'2026-03-08',6,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(348,'2026-05-03',5.9,'Routine checkup & diet evaluation','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(349,'2026-07-04',5.6,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(350,'2026-08-30',5.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(351,'2026-10-03',6.2,'Current logged weight','2026-10-02 00:33:40.871536',18);
INSERT INTO "WEIGHT_HISTORY" VALUES(352,'2025-11-08',2.1,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(353,'2026-01-08',2.03,'Quarterly weight & body condition score check','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(354,'2026-03-07',2.05,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(355,'2026-05-03',1.95,'Routine checkup & diet evaluation','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(356,'2026-07-03',1.91,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(357,'2026-09-03',1.92,'Pre-seasonal wellness examination','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(358,'2026-10-01',2.1,'Current logged weight','2026-10-02 00:33:40.880134',17);
INSERT INTO "WEIGHT_HISTORY" VALUES(359,'2025-11-09',6.6,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(360,'2026-01-08',6.9,'Quarterly weight & body condition score check','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(361,'2026-03-03',7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(362,'2026-05-04',6.5,'Routine checkup & diet evaluation','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(363,'2026-07-02',6.7,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(364,'2026-08-31',7.1,'Pre-seasonal wellness examination','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(365,'2026-10-02',6.8,'Current logged weight','2026-10-02 00:33:40.887275',16);
INSERT INTO "WEIGHT_HISTORY" VALUES(366,'2025-11-08',18.4,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(367,'2026-01-08',17.6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(368,'2026-03-05',17.2,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(369,'2026-05-08',16.6,'Routine checkup & diet evaluation','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(370,'2026-07-05',16.7,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(371,'2026-09-05',16.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(372,'2026-10-05',18,'Current logged weight','2026-10-02 00:33:40.894684',15);
INSERT INTO "WEIGHT_HISTORY" VALUES(373,'2025-11-08',5.4,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(374,'2026-01-06',5.6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(375,'2026-03-07',5.7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(376,'2026-05-06',5.4,'Routine checkup & diet evaluation','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(377,'2026-07-07',5.4,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(378,'2026-08-30',5.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(379,'2026-10-04',5.5,'Current logged weight','2026-10-02 00:33:40.901199',14);
INSERT INTO "WEIGHT_HISTORY" VALUES(380,'2025-11-07',9.4,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(381,'2026-01-04',9.4,'Quarterly weight & body condition score check','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(382,'2026-03-09',9.8,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(383,'2026-05-06',9.1,'Routine checkup & diet evaluation','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(384,'2026-07-01',9.6,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(385,'2026-09-01',9.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(386,'2026-10-01',9.5,'Current logged weight','2026-10-02 00:33:40.909389',13);
INSERT INTO "WEIGHT_HISTORY" VALUES(387,'2025-11-08',0.1,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(388,'2026-01-07',0.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(389,'2026-03-06',0.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(390,'2026-05-07',0.1,'Routine checkup & diet evaluation','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(391,'2026-07-02',0.1,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(392,'2026-09-01',0.1,'Pre-seasonal wellness examination','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(393,'2026-10-05',0.1,'Current logged weight','2026-10-02 00:33:40.917097',12);
INSERT INTO "WEIGHT_HISTORY" VALUES(394,'2025-11-08',11.7,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.924245',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(395,'2026-01-03',12,'Quarterly weight & body condition score check','2026-10-02 00:33:40.924245',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(396,'2026-03-04',12.3,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.925247',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(397,'2026-05-02',11.8,'Routine checkup & diet evaluation','2026-10-02 00:33:40.925247',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(398,'2026-07-06',11.9,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.925247',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(399,'2026-09-01',12.3,'Pre-seasonal wellness examination','2026-10-02 00:33:40.925247',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(400,'2026-10-01',12,'Current logged weight','2026-10-02 00:33:40.925247',11);
INSERT INTO "WEIGHT_HISTORY" VALUES(401,'2025-11-04',29.3,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(402,'2026-01-05',29.9,'Quarterly weight & body condition score check','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(403,'2026-03-09',30.5,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(404,'2026-05-07',29,'Routine checkup & diet evaluation','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(405,'2026-07-06',30.4,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(406,'2026-08-31',30.8,'Pre-seasonal wellness examination','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(407,'2026-10-04',30,'Current logged weight','2026-10-02 00:33:40.932771',10);
INSERT INTO "WEIGHT_HISTORY" VALUES(408,'2025-11-09',3.81,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(409,'2026-01-05',3.74,'Quarterly weight & body condition score check','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(410,'2026-03-09',3.7,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(411,'2026-05-07',3.6,'Routine checkup & diet evaluation','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(412,'2026-07-02',3.57,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(413,'2026-08-30',3.46,'Pre-seasonal wellness examination','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(414,'2026-10-02',3.8,'Current logged weight','2026-10-02 00:33:40.938958',9);
INSERT INTO "WEIGHT_HISTORY" VALUES(415,'2025-11-07',32.6,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(416,'2026-01-05',34.1,'Quarterly weight & body condition score check','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(417,'2026-03-07',35.1,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(418,'2026-05-03',33,'Routine checkup & diet evaluation','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(419,'2026-07-07',34,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(420,'2026-09-05',34.4,'Pre-seasonal wellness examination','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(421,'2026-10-01',34,'Current logged weight','2026-10-02 00:33:40.947868',8);
INSERT INTO "WEIGHT_HISTORY" VALUES(422,'2025-11-04',1.8,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(423,'2026-01-04',1.66,'Quarterly weight & body condition score check','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(424,'2026-03-09',1.56,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(425,'2026-05-04',1.35,'Routine checkup & diet evaluation','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(426,'2026-07-02',1.28,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(427,'2026-09-01',1.17,'Pre-seasonal wellness examination','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(428,'2026-10-05',1.8,'Current logged weight','2026-10-02 00:33:40.954624',7);
INSERT INTO "WEIGHT_HISTORY" VALUES(429,'2025-11-07',4.17,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(430,'2026-01-07',4.03,'Quarterly weight & body condition score check','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(431,'2026-03-03',4,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(432,'2026-05-05',3.95,'Routine checkup & diet evaluation','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(433,'2026-07-01',3.81,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(434,'2026-09-05',3.75,'Pre-seasonal wellness examination','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(435,'2026-10-03',4.2,'Current logged weight','2026-10-02 00:33:40.962223',6);
INSERT INTO "WEIGHT_HISTORY" VALUES(436,'2025-11-04',27.6,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(437,'2026-01-03',28.6,'Quarterly weight & body condition score check','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(438,'2026-03-03',29.9,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(439,'2026-05-08',28,'Routine checkup & diet evaluation','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(440,'2026-07-06',29,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(441,'2026-09-04',29.5,'Pre-seasonal wellness examination','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(442,'2026-10-01',28.5,'Current logged weight','2026-10-02 00:33:40.968775',5);
INSERT INTO "WEIGHT_HISTORY" VALUES(443,'2025-11-03',11.8,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(444,'2026-01-05',11.8,'Quarterly weight & body condition score check','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(445,'2026-03-06',12.5,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(446,'2026-05-02',11.6,'Routine checkup & diet evaluation','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(447,'2026-07-05',11.8,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(448,'2026-09-04',12.6,'Pre-seasonal wellness examination','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(449,'2026-10-01',12,'Current logged weight','2026-10-02 00:33:40.972271',4);
INSERT INTO "WEIGHT_HISTORY" VALUES(450,'2025-11-06',34.9,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(451,'2026-01-03',35.8,'Quarterly weight & body condition score check','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(452,'2026-03-09',37.8,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(453,'2026-05-08',35.6,'Routine checkup & diet evaluation','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(454,'2026-07-07',36.3,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(455,'2026-09-04',37.4,'Pre-seasonal wellness examination','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(456,'2026-10-03',36.5,'Current logged weight','2026-10-02 00:33:40.977697',3);
INSERT INTO "WEIGHT_HISTORY" VALUES(457,'2025-11-06',4.24,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(458,'2026-01-06',4.03,'Quarterly weight & body condition score check','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(459,'2026-03-07',3.98,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(460,'2026-05-03',3.99,'Routine checkup & diet evaluation','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(461,'2026-07-05',3.86,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(462,'2026-09-01',3.74,'Pre-seasonal wellness examination','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(463,'2026-09-29',4.2,'Current logged weight','2026-10-02 00:33:40.982219',2);
INSERT INTO "WEIGHT_HISTORY" VALUES(464,'2025-11-06',29.7,'Annual comprehensive wellness check & baseline','2026-10-02 00:33:40.988926',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(465,'2026-01-03',31.5,'Quarterly weight & body condition score check','2026-10-02 00:33:40.989932',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(466,'2026-03-07',32.4,'Mid-year preventive care & booster weigh-in','2026-10-02 00:33:40.989932',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(467,'2026-05-05',29.7,'Routine checkup & diet evaluation','2026-10-02 00:33:40.989932',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(468,'2026-07-01',31.4,'Grooming visit weigh-in & health check','2026-10-02 00:33:40.989932',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(469,'2026-09-05',32.4,'Pre-seasonal wellness examination','2026-10-02 00:33:40.989932',1);
INSERT INTO "WEIGHT_HISTORY" VALUES(470,'2026-09-29',31,'Current logged weight','2026-10-02 00:33:40.989932',1);
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES(5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES(6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES(7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES(8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES(9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES(10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES(11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES(12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES(17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES(18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES(19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES(21,6,'add_user','Can add User');
INSERT INTO "auth_permission" VALUES(22,6,'change_user','Can change User');
INSERT INTO "auth_permission" VALUES(23,6,'delete_user','Can delete User');
INSERT INTO "auth_permission" VALUES(24,6,'view_user','Can view User');
INSERT INTO "auth_permission" VALUES(25,7,'add_pet','Can add Pet');
INSERT INTO "auth_permission" VALUES(26,7,'change_pet','Can change Pet');
INSERT INTO "auth_permission" VALUES(27,7,'delete_pet','Can delete Pet');
INSERT INTO "auth_permission" VALUES(28,7,'view_pet','Can view Pet');
INSERT INTO "auth_permission" VALUES(29,8,'add_caretakerprofile','Can add Caretaker Profile');
INSERT INTO "auth_permission" VALUES(30,8,'change_caretakerprofile','Can change Caretaker Profile');
INSERT INTO "auth_permission" VALUES(31,8,'delete_caretakerprofile','Can delete Caretaker Profile');
INSERT INTO "auth_permission" VALUES(32,8,'view_caretakerprofile','Can view Caretaker Profile');
INSERT INTO "auth_permission" VALUES(33,9,'add_booking','Can add Booking');
INSERT INTO "auth_permission" VALUES(34,9,'change_booking','Can change Booking');
INSERT INTO "auth_permission" VALUES(35,9,'delete_booking','Can delete Booking');
INSERT INTO "auth_permission" VALUES(36,9,'view_booking','Can view Booking');
INSERT INTO "auth_permission" VALUES(37,10,'add_review','Can add Review');
INSERT INTO "auth_permission" VALUES(38,10,'change_review','Can change Review');
INSERT INTO "auth_permission" VALUES(39,10,'delete_review','Can delete Review');
INSERT INTO "auth_permission" VALUES(40,10,'view_review','Can view Review');
INSERT INTO "auth_permission" VALUES(41,11,'add_adoptionlisting','Can add Adoption Listing');
INSERT INTO "auth_permission" VALUES(42,11,'change_adoptionlisting','Can change Adoption Listing');
INSERT INTO "auth_permission" VALUES(43,11,'delete_adoptionlisting','Can delete Adoption Listing');
INSERT INTO "auth_permission" VALUES(44,11,'view_adoptionlisting','Can view Adoption Listing');
INSERT INTO "auth_permission" VALUES(45,12,'add_matchprofile','Can add Match Profile');
INSERT INTO "auth_permission" VALUES(46,12,'change_matchprofile','Can change Match Profile');
INSERT INTO "auth_permission" VALUES(47,12,'delete_matchprofile','Can delete Match Profile');
INSERT INTO "auth_permission" VALUES(48,12,'view_matchprofile','Can view Match Profile');
INSERT INTO "auth_permission" VALUES(49,13,'add_matchrequest','Can add Match Request');
INSERT INTO "auth_permission" VALUES(50,13,'change_matchrequest','Can change Match Request');
INSERT INTO "auth_permission" VALUES(51,13,'delete_matchrequest','Can delete Match Request');
INSERT INTO "auth_permission" VALUES(52,13,'view_matchrequest','Can view Match Request');
INSERT INTO "auth_permission" VALUES(53,14,'add_allergyrecord','Can add Allergy Record');
INSERT INTO "auth_permission" VALUES(54,14,'change_allergyrecord','Can change Allergy Record');
INSERT INTO "auth_permission" VALUES(55,14,'delete_allergyrecord','Can delete Allergy Record');
INSERT INTO "auth_permission" VALUES(56,14,'view_allergyrecord','Can view Allergy Record');
INSERT INTO "auth_permission" VALUES(57,15,'add_healthrecord','Can add Health Record');
INSERT INTO "auth_permission" VALUES(58,15,'change_healthrecord','Can change Health Record');
INSERT INTO "auth_permission" VALUES(59,15,'delete_healthrecord','Can delete Health Record');
INSERT INTO "auth_permission" VALUES(60,15,'view_healthrecord','Can view Health Record');
INSERT INTO "auth_permission" VALUES(61,16,'add_medicinerecord','Can add Medicine Record');
INSERT INTO "auth_permission" VALUES(62,16,'change_medicinerecord','Can change Medicine Record');
INSERT INTO "auth_permission" VALUES(63,16,'delete_medicinerecord','Can delete Medicine Record');
INSERT INTO "auth_permission" VALUES(64,16,'view_medicinerecord','Can view Medicine Record');
INSERT INTO "auth_permission" VALUES(65,17,'add_vaccinationrecord','Can add Vaccination Record');
INSERT INTO "auth_permission" VALUES(66,17,'change_vaccinationrecord','Can change Vaccination Record');
INSERT INTO "auth_permission" VALUES(67,17,'delete_vaccinationrecord','Can delete Vaccination Record');
INSERT INTO "auth_permission" VALUES(68,17,'view_vaccinationrecord','Can view Vaccination Record');
INSERT INTO "auth_permission" VALUES(69,18,'add_weightrecord','Can add Weight History Record');
INSERT INTO "auth_permission" VALUES(70,18,'change_weightrecord','Can change Weight History Record');
INSERT INTO "auth_permission" VALUES(71,18,'delete_weightrecord','Can delete Weight History Record');
INSERT INTO "auth_permission" VALUES(72,18,'view_weightrecord','Can view Weight History Record');
INSERT INTO "auth_permission" VALUES(73,19,'add_notification','Can add Notification');
INSERT INTO "auth_permission" VALUES(74,19,'change_notification','Can change Notification');
INSERT INTO "auth_permission" VALUES(75,19,'delete_notification','Can delete Notification');
INSERT INTO "auth_permission" VALUES(76,19,'view_notification','Can view Notification');
INSERT INTO "auth_permission" VALUES(77,20,'add_lostpetreport','Can add Lost Pet Report');
INSERT INTO "auth_permission" VALUES(78,20,'change_lostpetreport','Can change Lost Pet Report');
INSERT INTO "auth_permission" VALUES(79,20,'delete_lostpetreport','Can delete Lost Pet Report');
INSERT INTO "auth_permission" VALUES(80,20,'view_lostpetreport','Can view Lost Pet Report');
INSERT INTO "auth_permission" VALUES(81,21,'add_lostpetsighting','Can add Lost Pet Sighting');
INSERT INTO "auth_permission" VALUES(82,21,'change_lostpetsighting','Can change Lost Pet Sighting');
INSERT INTO "auth_permission" VALUES(83,21,'delete_lostpetsighting','Can delete Lost Pet Sighting');
INSERT INTO "auth_permission" VALUES(84,21,'view_lostpetsighting','Can view Lost Pet Sighting');
INSERT INTO "auth_permission" VALUES(85,22,'add_chathistory','Can add Chat History');
INSERT INTO "auth_permission" VALUES(86,22,'change_chathistory','Can change Chat History');
INSERT INTO "auth_permission" VALUES(87,22,'delete_chathistory','Can delete Chat History');
INSERT INTO "auth_permission" VALUES(88,22,'view_chathistory','Can view Chat History');
INSERT INTO "auth_permission" VALUES(89,23,'add_recommendationlog','Can add Recommendation Log');
INSERT INTO "auth_permission" VALUES(90,23,'change_recommendationlog','Can change Recommendation Log');
INSERT INTO "auth_permission" VALUES(91,23,'delete_recommendationlog','Can delete Recommendation Log');
INSERT INTO "auth_permission" VALUES(92,23,'view_recommendationlog','Can view Recommendation Log');
INSERT INTO "auth_permission" VALUES(93,24,'add_breedscanlog','Can add Breed Scan Log');
INSERT INTO "auth_permission" VALUES(94,24,'change_breedscanlog','Can change Breed Scan Log');
INSERT INTO "auth_permission" VALUES(95,24,'delete_breedscanlog','Can delete Breed Scan Log');
INSERT INTO "auth_permission" VALUES(96,24,'view_breedscanlog','Can view Breed Scan Log');
INSERT INTO "auth_permission" VALUES(97,25,'add_payment','Can add Payment');
INSERT INTO "auth_permission" VALUES(98,25,'change_payment','Can change Payment');
INSERT INTO "auth_permission" VALUES(99,25,'delete_payment','Can delete Payment');
INSERT INTO "auth_permission" VALUES(100,25,'view_payment','Can view Payment');
INSERT INTO "auth_permission" VALUES(101,26,'add_adoptionpayment','Can add Adoption Payment');
INSERT INTO "auth_permission" VALUES(102,26,'change_adoptionpayment','Can change Adoption Payment');
INSERT INTO "auth_permission" VALUES(103,26,'delete_adoptionpayment','Can delete Adoption Payment');
INSERT INTO "auth_permission" VALUES(104,26,'view_adoptionpayment','Can view Adoption Payment');
INSERT INTO "auth_permission" VALUES(105,27,'add_adoptionrequest','Can add Adoption Request');
INSERT INTO "auth_permission" VALUES(106,27,'change_adoptionrequest','Can change Adoption Request');
INSERT INTO "auth_permission" VALUES(107,27,'delete_adoptionrequest','Can delete Adoption Request');
INSERT INTO "auth_permission" VALUES(108,27,'view_adoptionrequest','Can view Adoption Request');
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "USERS" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','permission');
INSERT INTO "django_content_type" VALUES(3,'auth','group');
INSERT INTO "django_content_type" VALUES(4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'sessions','session');
INSERT INTO "django_content_type" VALUES(6,'users','user');
INSERT INTO "django_content_type" VALUES(7,'pets','pet');
INSERT INTO "django_content_type" VALUES(8,'marketplace','caretakerprofile');
INSERT INTO "django_content_type" VALUES(9,'bookings','booking');
INSERT INTO "django_content_type" VALUES(10,'reviews','review');
INSERT INTO "django_content_type" VALUES(11,'adoption','adoptionlisting');
INSERT INTO "django_content_type" VALUES(12,'matchhub','matchprofile');
INSERT INTO "django_content_type" VALUES(13,'matchhub','matchrequest');
INSERT INTO "django_content_type" VALUES(14,'health','allergyrecord');
INSERT INTO "django_content_type" VALUES(15,'health','healthrecord');
INSERT INTO "django_content_type" VALUES(16,'health','medicinerecord');
INSERT INTO "django_content_type" VALUES(17,'health','vaccinationrecord');
INSERT INTO "django_content_type" VALUES(18,'health','weightrecord');
INSERT INTO "django_content_type" VALUES(19,'notifications','notification');
INSERT INTO "django_content_type" VALUES(20,'lostfound','lostpetreport');
INSERT INTO "django_content_type" VALUES(21,'lostfound','lostpetsighting');
INSERT INTO "django_content_type" VALUES(22,'chatbot','chathistory');
INSERT INTO "django_content_type" VALUES(23,'recommendations','recommendationlog');
INSERT INTO "django_content_type" VALUES(24,'breed_detection','breedscanlog');
INSERT INTO "django_content_type" VALUES(25,'bookings','payment');
INSERT INTO "django_content_type" VALUES(26,'adoption','adoptionpayment');
INSERT INTO "django_content_type" VALUES(27,'adoption','adoptionrequest');
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO "django_migrations" VALUES(1,'contenttypes','0001_initial','2026-08-23 07:06:01.047439');
INSERT INTO "django_migrations" VALUES(2,'contenttypes','0002_remove_content_type_name','2026-08-23 07:06:01.063056');
INSERT INTO "django_migrations" VALUES(3,'auth','0001_initial','2026-08-23 07:06:01.085521');
INSERT INTO "django_migrations" VALUES(4,'auth','0002_alter_permission_name_max_length','2026-08-23 07:06:01.101714');
INSERT INTO "django_migrations" VALUES(5,'auth','0003_alter_user_email_max_length','2026-08-23 07:06:01.112483');
INSERT INTO "django_migrations" VALUES(6,'auth','0004_alter_user_username_opts','2026-08-23 07:06:01.123610');
INSERT INTO "django_migrations" VALUES(7,'auth','0005_alter_user_last_login_null','2026-08-23 07:06:01.136002');
INSERT INTO "django_migrations" VALUES(8,'auth','0006_require_contenttypes_0002','2026-08-23 07:06:01.143140');
INSERT INTO "django_migrations" VALUES(9,'auth','0007_alter_validators_add_error_messages','2026-08-23 07:06:01.155064');
INSERT INTO "django_migrations" VALUES(10,'auth','0008_alter_user_username_max_length','2026-08-23 07:06:01.167616');
INSERT INTO "django_migrations" VALUES(11,'auth','0009_alter_user_last_name_max_length','2026-08-23 07:06:01.180065');
INSERT INTO "django_migrations" VALUES(12,'auth','0010_alter_group_name_max_length','2026-08-23 07:06:01.195781');
INSERT INTO "django_migrations" VALUES(13,'auth','0011_update_proxy_permissions','2026-08-23 07:06:01.206824');
INSERT INTO "django_migrations" VALUES(14,'auth','0012_alter_user_first_name_max_length','2026-08-23 07:06:01.220216');
INSERT INTO "django_migrations" VALUES(15,'users','0001_initial','2026-08-23 07:06:01.243488');
INSERT INTO "django_migrations" VALUES(16,'admin','0001_initial','2026-08-23 07:06:01.266971');
INSERT INTO "django_migrations" VALUES(17,'admin','0002_logentry_remove_auto_add','2026-08-23 07:06:01.282694');
INSERT INTO "django_migrations" VALUES(18,'admin','0003_logentry_add_action_flag_choices','2026-08-23 07:06:01.296322');
INSERT INTO "django_migrations" VALUES(19,'adoption','0001_initial','2026-08-23 07:06:01.306457');
INSERT INTO "django_migrations" VALUES(20,'adoption','0002_initial','2026-08-23 07:06:01.323909');
INSERT INTO "django_migrations" VALUES(21,'pets','0001_initial','2026-08-23 07:06:01.334546');
INSERT INTO "django_migrations" VALUES(22,'marketplace','0001_initial','2026-08-23 07:06:01.344940');
INSERT INTO "django_migrations" VALUES(23,'bookings','0001_initial','2026-08-23 07:06:01.354630');
INSERT INTO "django_migrations" VALUES(24,'bookings','0002_initial','2026-08-23 07:06:01.368908');
INSERT INTO "django_migrations" VALUES(25,'bookings','0003_initial','2026-08-23 07:06:01.397947');
INSERT INTO "django_migrations" VALUES(26,'breed_detection','0001_initial','2026-08-23 07:06:01.409894');
INSERT INTO "django_migrations" VALUES(27,'breed_detection','0002_initial','2026-08-23 07:06:01.435519');
INSERT INTO "django_migrations" VALUES(28,'chatbot','0001_initial','2026-08-23 07:06:01.452371');
INSERT INTO "django_migrations" VALUES(29,'chatbot','0002_initial','2026-08-23 07:06:01.476000');
INSERT INTO "django_migrations" VALUES(30,'health','0001_initial','2026-08-23 07:06:01.495216');
INSERT INTO "django_migrations" VALUES(31,'health','0002_initial','2026-08-23 07:06:01.600196');
INSERT INTO "django_migrations" VALUES(32,'lostfound','0001_initial','2026-08-23 07:06:01.623327');
INSERT INTO "django_migrations" VALUES(33,'lostfound','0002_initial','2026-08-23 07:06:01.647197');
INSERT INTO "django_migrations" VALUES(34,'marketplace','0002_initial','2026-08-23 07:06:01.670846');
INSERT INTO "django_migrations" VALUES(35,'matchhub','0001_initial','2026-08-23 07:06:01.694808');
INSERT INTO "django_migrations" VALUES(36,'matchhub','0002_initial','2026-08-23 07:06:01.716945');
INSERT INTO "django_migrations" VALUES(37,'notifications','0001_initial','2026-08-23 07:06:01.729142');
INSERT INTO "django_migrations" VALUES(38,'notifications','0002_initial','2026-08-23 07:06:01.756147');
INSERT INTO "django_migrations" VALUES(39,'pets','0002_initial','2026-08-23 07:06:01.783885');
INSERT INTO "django_migrations" VALUES(40,'recommendations','0001_initial','2026-08-23 07:06:01.816807');
INSERT INTO "django_migrations" VALUES(41,'recommendations','0002_initial','2026-08-23 07:06:01.846749');
INSERT INTO "django_migrations" VALUES(42,'reviews','0001_initial','2026-08-23 07:06:01.875851');
INSERT INTO "django_migrations" VALUES(43,'reviews','0002_initial','2026-08-23 07:06:01.903120');
INSERT INTO "django_migrations" VALUES(44,'sessions','0001_initial','2026-08-23 07:06:01.921174');
INSERT INTO "django_migrations" VALUES(45,'lostfound','0003_lostpetreport_alternate_contact_and_more','2026-10-07 17:13:54.231457');
INSERT INTO "django_migrations" VALUES(46,'lostfound','0004_lostpetreport_police_document_and_more','2026-10-07 17:26:44.128151');
INSERT INTO "django_migrations" VALUES(47,'bookings','0004_booking_payment_status_payment','2026-10-15 22:20:54.143997');
INSERT INTO "django_migrations" VALUES(48,'adoption','0003_adoptionlisting_adopter_and_more','2026-10-15 23:06:21.449469');
INSERT INTO "django_migrations" VALUES(49,'adoption','0004_adoptionrequest','2026-10-15 23:20:56.824194');
INSERT INTO "django_migrations" VALUES(50,'bookings','0005_booking_arrival_time_booking_emergency_fee_and_more','2026-10-18 11:18:48.219437');
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "django_session" VALUES('h2i6trx79d61cro9fe7whzcz2beb1rsk','.eJxVjr0OgzAQg98lc4mO_JCkY_c-A7pcLoW2IhKBqeq7F1QWRtufLX8EDbj0lWsdy9SPSVxFVtAFrbjRFKExznWND-wbAz52TgNYZnERPa7L0K-V539Nnb2I9OJpD9ITp0eRVKZlHqPcEXmkVd5L4vftYE8DA9Zhb-c2gQWiGCgbCgR6P6ISKesUW-0CGs82pRYiZgzbd6M8arupmLz4_gCc6khm:1wy3Su:QikAIIturGP8mRMJiRISXx538Af2mYdVIO_aGZ0-cXQ','2026-09-06 08:22:04.713110');
INSERT INTO "django_session" VALUES('ar819fsoz9kdk8ukfrprnmij1i5jhrfk','.eJxVjMsOwiAURP-FtSGUhwWX7vsN5D5AqoYmpV0Z_11JutDlzDkzLxFh30rcW1rjzOIitDj9dgj0SLUDvkO9LZKWuq0zyq7IgzY5LZye18P9OyjQSl_ngZVTRBgoWwqkjFUeNZN2o07OjAGsT455UAgZwjkYqz0Y903IXrw_-xU4iQ:1wy5RS:Mt4LfhO3cDpGQzIpuLG5NLTRbN6lBpgqsokfKiq6AWg','2026-09-06 10:28:42.596250');
INSERT INTO "django_session" VALUES('be4ypaebsvmblkil7kjj9z4s4dwuu0a8','.eJxVjMsOwiAQRf-FtSFQHgGX7v0GMsMMUjWQlHZl_Hdt0oVu7znnvkSCba1pG7ykmcRZaHH63RDyg9sO6A7t1mXubV1mlLsiDzrktRM_L4f7d1Bh1G896Qwhe1sKeyzGkrPKkwqxGA2mkI0RtWUMCqLHTBOQKQxO5UjRGRTvD_xqOMI:1x672N:tNUaWf_UsG8M-aT7cKOQIupMhOc0IDMrcm1j1GWVtpE','2026-09-28 13:47:59.877652');
INSERT INTO "django_session" VALUES('mkadyhvfmvhh2t0yhbfg53ax831if7fr','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1x677r:uEhmlkZr4pUeLmOqddPPh_hoUFarJXDekkvPBXjfabg','2026-09-28 13:53:39.330604');
INSERT INTO "django_session" VALUES('fupdl4xr0l26ejnnc3k9jg8bvq14re6z','.eJxVjL0KwjAURt8ls5Q0N7-OgqM4OYeb3FtSbCs0dhLfXQMddDzn-zgvEXF7lrhVXuNI4ihAisOvTJjvvLSlYe12rt15xnG6rrevXXDmy4N4Ou3nv0LBWlpYK2nJkfNS6d6zN9kGiwTapOxgIAIC51PQiYaggkEbKJMmZGd6UOL9AU1HOJQ:1x678B:nivcgIbFcUAWzOmJ4XJgKmOULaF8ft0aQ3tQpnHhA_Q','2026-09-28 13:53:59.602799');
INSERT INTO "django_session" VALUES('dxjjs9srbiu1p7kyjextn90urvvv6wsl','.eJxVjD0LwjAQhv9LZilJk4bEUXAUJ-dwl7sjxX5AYyfxv9tCBx2f5_14qwTrq6S18pJ6Umdl1OnXIeQnT3uwY20Ors11hH64L4_NTjDybSYeLkf576FALdu8NRlC9k6EPYp11DntSYco1oAVcjGicYxBQ_SYqQWywtDpHCl2FtXnC1l4OWs:1xEVXm:oVFlXcevpHHg4UiyVVDa5xS6dWI0Pw--CoKopMyrWB8','2026-10-21 17:35:06.881833');
INSERT INTO "django_session" VALUES('wkgcew9ndtbtvisao246stzk0j98a6t5','e30:1xHU4j:hUW6jAi7uanTsK2YGXo99L4UE9mv5ewIQp-ZK0wSJRg','2026-10-29 22:37:25.436222');
INSERT INTO "django_session" VALUES('20mrfglfpnzs0n86szogm6durhdckmdx','e30:1xHU8K:wEKkZFY2wUSr2_LEmicJ7acM7D_FEoR71vwfypFor7U','2026-10-29 22:41:08.951672');
INSERT INTO "django_session" VALUES('qu5skxio15eejk1774cxlw1y9tkv1hx4','.eJxVjD0LwjAQhv9LZilJk4bEUXAUJ-dwl7sjxX5AYyfxv9tCBx2f5_14qwTrq6S18pJ6Umdl1OnXIeQnT3uwY20Ors11hH64L4_NTjDybSYeLkf576FALdu8NRlC9k6EPYp11DntSYco1oAVcjGicYxBQ_SYqQWywtDpHCl2FtXnC1l4OWs:1xHUAC:I4S-5Q22NsTWP5OzujPpQ5u02LBDR_OrgU77bUwVAG8','2026-10-29 22:43:04.603368');
INSERT INTO "django_session" VALUES('hyxqkah0zf2kuoma9jbofxvdbyf4zlm4','.eJxVjD0LwjAQhv9LZimXNNdLHAVHcXIOFy8hxbZCYyfxv9tCBx2f5_14q8DLq4Slpjn0oo4KjTr8ysj3R5q2ZMPa7Fyb88j9cJ1vq514TJenpOG0l_8eCteyzluHoLmL2nvRHWcGyzY7ZNO2jiIZJEIbDQElDZmSaEvirQfjBUHU5ws-zzeT:1xHUBq:AAxx76Cg7GieR4_dsGGeS-Y_Vy_tIw9B5xJqPGti3SI','2026-10-29 22:44:46.439393');
INSERT INTO "django_session" VALUES('w0oqr39xzu81haehsx5chy9gkhp4kyth','.eJxVjLsKwjAUht8ls5TcTi6OgqM4OYeT5JQUe4HGTuK7m0IHnX6-__ZmAbdXCVulNQyZnRkodvo1I6YnzXuyY-0Ort11wmG8r4_mzjjRbck0Xo7y30PBWtq8jyCJLAkkEY0Dj6gIrbESmgD2SDpx5EJmFXVyPBnrXFJccO2zB_b5Aou6OQY:1xHUBr:rCOM8FIHcDxOtypYP5alHqfnL5pThlIP6T7nSvwx4mY','2026-10-29 22:44:47.048794');
INSERT INTO "django_session" VALUES('e3c5ofhwiaresmjm99q0fhyuxy5vj53p','.eJxVjLsOgjAUht-lsyGlF2kdTRwNk3Nzes5pSgRMqEzEd7ckDDp-33_ZRID1ncNaeAkDiYtQ4vTrIuCT5z3YsTQHl-Y2wTD2y6PaGSa-v4jH61H-e8hQcp1TaklaiRg9JoMepTbSRUWobKfY6s6DcWyJWhkhgT97bZQDbStFcuLzBVgkOTI:1xHUDG:jKTvO9hPetl-OWTgu2frZzTscEKul_TV7aTErneGAbE','2026-10-29 22:46:14.024561');
INSERT INTO "django_session" VALUES('fdeme1ua104t6z0o721mqx5injuedprz','.eJxVjLsOgjAUht-lsyGlF2kdTRwNk3Nzes5pSgRMqEzEd7ckDDp-33_ZRID1ncNaeAkDiYtQ4vTrIuCT5z3YsTQHl-Y2wTD2y6PaGSa-v4jH61H-e8hQcp1TaklaiRg9JoMepTbSRUWobKfY6s6DcWyJWhkhgT97bZQDbStFcuLzBVgkOTI:1xHUDO:6oYJWh25Y4HQo6S-Md4h2_bAa0c29wDuioFpelFnIL4','2026-10-29 22:46:22.923757');
INSERT INTO "django_session" VALUES('9f8mp6mtozfa10onfjqhozylcngjh43h','.eJxVjLsOgjAUht-lsyGlF2kdTRwNk3Nzes5pSgRMqEzEd7ckDDp-33_ZRID1ncNaeAkDiYtQ4vTrIuCT5z3YsTQHl-Y2wTD2y6PaGSa-v4jH61H-e8hQcp1TaklaiRg9JoMepTbSRUWobKfY6s6DcWyJWhkhgT97bZQDbStFcuLzBVgkOTI:1xHUDm:NDcc7vPBkcfX-coBJgLDw5_mW9Hln9MZ4uboW-5tgHo','2026-10-29 22:46:46.761265');
INSERT INTO "django_session" VALUES('k2p2axhn67bjmrd9i509b0re7h2nqncv','.eJxVjLsKwkAQRf9lawn7mtmspWApVtZhdmdCgnlA1lTiv5tACi3PuY-3amh9dc1aZGl6VmflnTr9ykT5KdOe7Fiqg0t1Hakf7stjsxONcptZhstR_nvoqHTbHMQDWXScHIoTZzOhtgEANFsTfEBKtbYEzmtsMbNhBG5j0tGbWBv1-QJHYTe1:1xI8zd:e0hlJrDZ5h_NKgdeds34hn7ZGJud2HFnp0EAGcWBqF4','2026-10-31 18:18:53.987861');
INSERT INTO "django_session" VALUES('t0nicp4ayu6t1p33yyrnhj73uqq7fo25','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xI9Pl:51weSNQrHtv3VUFaW2TTpDYw_yr6Gl2i_kCgTSgNGd8','2026-10-31 18:45:53.461361');
INSERT INTO "django_session" VALUES('p7i020jdct6cwubn0jq9kikf32uq72x5','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xI9Rs:eNy8O84UlL5-L8OoWJR8BkTaSZDZKPYwMqQLEBsUfAc','2026-10-31 18:48:04.499325');
INSERT INTO "django_session" VALUES('3i7nosdgy99uxhefpdtj8h38zi54uikj','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIJob:19SwZ-8d2xdlyKjn4fCjoZEc7U05cp-_LTy1-OeuosQ','2026-11-01 05:52:13.023253');
INSERT INTO "django_session" VALUES('jtksox7c5oifl4hvtpc70yeedpubf0oy','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIKSl:YoImX9QH3N9Fhffo7Rke-DWo9xCBKeAn21plpnQsMgc','2026-11-01 06:33:43.835950');
INSERT INTO "django_session" VALUES('z0v2ot7zvz1tzlezg2bcs0ztf3k312gi','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIKuS:huJhlZw0wJrKMulLTHgo3hcrmG3OXjmfp_6orvNzW44','2026-11-01 07:02:20.069832');
INSERT INTO "django_session" VALUES('ec78x9ym1e2kgw535tk6mikmq76baamh','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIKuz:UetsSRSTNdDT8ABs0Sq0WVMBhl1U9qhH0qmSdB6ojUU','2026-11-01 07:02:53.317193');
INSERT INTO "django_session" VALUES('i9c10rmoxf4w3e1vvjd4tmri9s71n1qn','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIMK1:Sf163Q9NR3tbY7Q0GYM0UyYz6285teDTkbAV_PzRQ7M','2026-11-01 08:32:49.391046');
INSERT INTO "django_session" VALUES('bd6vkxnyi774nllxot8u4h49bej3ed40','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIOHx:jnYsTV0uez2jINiGPmvZDUJtAiVKi_DBTnxRD5SgZi8','2026-11-01 10:38:49.010345');
INSERT INTO "django_session" VALUES('rg3s04eef42h80d5kr47kw8hwkq9gt9t','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIP4U:zxby4iwz8ng39l-9SBws-A2Lomo72AM6M6hmO8zPo6A','2026-11-01 11:28:58.130676');
INSERT INTO "django_session" VALUES('3xb9zg0y2bblk0n3kzuebiyid2ayqyo0','.eJxVjD0LwjAQhv9LZimXpEmNo-AoTs7hLrkjxbZCYyfxv9tCBx2f5_14q4jLq8Sl8hz7rE5Kgzr8SsL04GlLNqzNzrW5jNgPt_m-2glHvj4zD-e9_PdQsJZ1Tt44tjYb54NgF3SQFojJ6cxw1JCdtdYnm9h0RNJmYuMSgDAAihH1-QJgdDki:1xIP5Z:7PPJxiYRowDSMuY9ukcBqiRImlblbiTaJeOk7A4q8EM','2026-11-01 11:30:05.328707');
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
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('django_migrations',50);
INSERT INTO "sqlite_sequence" VALUES('django_content_type',27);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',108);
INSERT INTO "sqlite_sequence" VALUES('auth_group',0);
INSERT INTO "sqlite_sequence" VALUES('django_admin_log',0);
INSERT INTO "sqlite_sequence" VALUES('WEIGHT_HISTORY',470);
INSERT INTO "sqlite_sequence" VALUES('VACCINATIONS',109);
INSERT INTO "sqlite_sequence" VALUES('MEDICINES',17);
INSERT INTO "sqlite_sequence" VALUES('HEALTH_RECORDS',47);
INSERT INTO "sqlite_sequence" VALUES('ALLERGIES',4);
INSERT INTO "sqlite_sequence" VALUES('CARETAKERS',25);
INSERT INTO "sqlite_sequence" VALUES('MATCH_PROFILES',2);
INSERT INTO "sqlite_sequence" VALUES('NOTIFICATIONS',21);
INSERT INTO "sqlite_sequence" VALUES('PETS',53);
INSERT INTO "sqlite_sequence" VALUES('RECOMMENDATIONS',27);
INSERT INTO "sqlite_sequence" VALUES('REVIEWS',26);
INSERT INTO "sqlite_sequence" VALUES('USERS',55);
INSERT INTO "sqlite_sequence" VALUES('MATCH_REQUESTS',1);
INSERT INTO "sqlite_sequence" VALUES('LOST_PET_SIGHTINGS',10);
INSERT INTO "sqlite_sequence" VALUES('CHAT_HISTORY',37);
INSERT INTO "sqlite_sequence" VALUES('BREED_SCANS',27);
INSERT INTO "sqlite_sequence" VALUES('LOST_PETS',19);
INSERT INTO "sqlite_sequence" VALUES('ADOPTION_LISTINGS',24);
INSERT INTO "sqlite_sequence" VALUES('PAYMENTS',5);
INSERT INTO "sqlite_sequence" VALUES('BOOKINGS',47);
COMMIT;
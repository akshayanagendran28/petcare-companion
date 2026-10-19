# Database Architecture - Pet Care Companion

The primary database architecture for the **Pet Care Companion** platform is **MongoDB Atlas (Cloud NoSQL Document Store)**.

The system is architected as follows:
1. **MongoDB Atlas (Primary Persistent Database):**
   - 22+ Collections storing all domain models (Users, Pets, Caretakers, Bookings, Health records, Vaccinations, Lost & Found, Chat, Recommendations, Breed AI scans, etc.).
   - Connection managed in `backend/config/mongodb.py`.
   - Real-time live synchronization via `backend/config/mongo_signals.py`.
2. **Cloud PostgreSQL (Optional Production Relational Database):**
   - Connected automatically via `DATABASE_URL` on Render.
3. **Pure In-Memory Shared Cache:**
   - Zero on-disk SQLite files.
   - Restored and synced dynamically from MongoDB Atlas collections via `python manage.py restore_from_mongodb`.

---

## Directory Structure

```
database/
├── schema.sql                 # Extracted SQL schema definitions (CREATE TABLE, INDEX, CONSTRAINTS)
├── schema_dump.sql            # Full SQL database dump
├── README.md                  # This documentation file
└── oracle/                    # Oracle Database DDL and Setup Assets
```

---

## Common Database Management Commands

Run all commands from either the project root or the `backend/` folder:

- **Sync All Tables to MongoDB Atlas:**
  ```bash
  python manage.py sync_to_mongodb
  ```

- **Restore All Collections from MongoDB Atlas:**
  ```bash
  python manage.py restore_from_mongodb
  ```

- **Apply Pending Migrations:**
  ```bash
  python manage.py migrate
  ```

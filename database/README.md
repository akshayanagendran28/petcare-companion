# Database Architecture - Pet Care Companion

The `database/` directory manages data persistence, relational schemas, migrations, and database engine configurations for the **Pet Care Companion** platform.

The system is architected to seamlessly support two enterprise database engines:
1. **SQLite 3** (Default for local development, zero-configuration setup, and testing).
2. **Oracle Database** (Enterprise edition: 19c / 21c / 23ai / Oracle Free XE for production scalability).

---

## Directory Structure

```
database/
├── db.sqlite3                 # Active SQLite database file (contains pre-seeded demo accounts)
├── schema.sql                 # Extracted SQL schema definitions (CREATE TABLE, INDEX, CONSTRAINTS)
├── schema_dump.sql            # Full SQL database dump including schema and pre-populated seed data
├── README.md                  # This documentation file
└── oracle/                    # Oracle Database DDL and Setup Assets
    ├── schema_ddl.sql         # Oracle SQL DDL script for tables, sequences, triggers, and foreign keys
    └── oracle_setup_guide.md  # Step-by-step connection guide for Oracle Free XE / Cloud ADB
```

---

## Database Configuration

The application database connection is centrally controlled in `backend/config/settings.py`.

### 1. SQLite Engine (Default)
When `USE_ORACLE` is `False` or unset, Django automatically targets:
```python
DB_FILE = PROJECT_ROOT / 'database' / 'db.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE,
    }
}
```

### 2. Oracle Database Engine (Production)
To switch to Oracle Database, set the environment variable:
```bash
set USE_ORACLE=True
set ORACLE_DB_SERVICE_NAME=FREEPDB1
set ORACLE_DB_USER=pet_care_user
set ORACLE_DB_PASSWORD=PetCare123#
set ORACLE_DB_HOST=localhost
set ORACLE_DB_PORT=1521
```

---

## Common Database Management Commands

Run all commands from either the project root or the `backend/` folder:

- **Apply Pending Migrations:**
  ```bash
  python manage.py migrate
  ```

- **Create New Migrations after Model Edits:**
  ```bash
  python manage.py makemigrations
  ```

- **Export Schema Dump:**
  ```bash
  python -c "import sqlite3; con = sqlite3.connect('database/db.sqlite3'); [print(line) for line in con.iterdump()]" > database/schema_dump.sql
  ```

- **Launch Interactive Database Shell:**
  ```bash
  python manage.py dbshell
  ```

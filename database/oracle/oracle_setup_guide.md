# Oracle Database Setup Guide for Pet Care Companion

This project is architected specifically for **Oracle Database** (Oracle 19c, 21c, 23ai, or Oracle Database Express Edition XE / Free).

---

## 1. Prerequisites

1. **Oracle Database Installed**: Either locally (Oracle XE / Oracle 23ai Free) or an Oracle Autonomous Cloud Database instance.
2. **Python Oracle Connector**: `python-oracledb` (already included in `requirements.txt`).
3. **Database Listener Running**: Ensure port `1521` (default) is open and accessible.

---

## 2. Oracle User & Tablespace Setup

Log in to SQL*Plus or SQL Developer as `SYSDBA`:

```sql
sqlplus sys/your_sys_password@localhost:1521/FREEPDB1 as sysdba
```
*(Replace `FREEPDB1` or `XEPDB1` or `ORCLPDB` with your Pluggable Database service name).*

Execute the following commands to create a dedicated user and grant permissions:

```sql
-- Create user for Pet Care Companion
CREATE USER pet_care_user IDENTIFIED BY PetCare123#
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON users;

-- Grant required roles and privileges
GRANT CONNECT, RESOURCE TO pet_care_user;
GRANT CREATE SESSION TO pet_care_user;
GRANT CREATE TABLE TO pet_care_user;
GRANT CREATE VIEW TO pet_care_user;
GRANT CREATE SEQUENCE TO pet_care_user;
GRANT CREATE TRIGGER TO pet_care_user;
GRANT CREATE PROCEDURE TO pet_care_user;
GRANT UNLIMITED TABLESPACE TO pet_care_user;

COMMIT;
```

---

## 3. Configuring Django Settings for Oracle

In `config/settings.py` (or via `.env` file):

Set the database environment variables:
```bash
USE_ORACLE=True
ORACLE_DB_USER=pet_care_user
ORACLE_DB_PASSWORD=PetCare123#
ORACLE_DB_HOST=localhost
ORACLE_DB_PORT=1521
ORACLE_DB_SERVICE_NAME=FREEPDB1
```

Django will use `django.db.backends.oracle` with `python-oracledb` running in modern Thin mode (no Oracle Instant Client required) or Thick mode.

---

## 4. Running Migrations & Seeding Sample Data

Once the Oracle connection is configured:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

To run the pure SQL schema directly into Oracle SQL*Plus:
```bash
sqlplus pet_care_user/PetCare123#@localhost:1521/FREEPDB1 @oracle_sql/schema_ddl.sql
```

---

## 5. Development Fallback Switch

For quick testing or if Oracle DB is not running on a host during rapid local UI preview, set:
```bash
USE_ORACLE=False
```
This automatically runs SQLite with standard compatibility so developers can demo features instantly anywhere.

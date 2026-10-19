# MongoDB Atlas Document Store - Pet Care Companion

The **Pet Care Companion** platform supports a polyglot persistence architecture:
- **Relational Layer (PostgreSQL / SQLite / Oracle):** Handles ACID-compliant user authentication, caretaker listings, bookings, and financial payment transactions.
- **NoSQL Document Layer (MongoDB Atlas):** Handles dynamic unstructured documents, time-series telemetry, and AI/ML model logging:
  - 🤖 **`chat_conversations`**: Multi-turn AI chat history, user prompts, model responses, and navigation actions.
  - 📊 **`pet_vital_logs`**: Time-series biometric logs, weight curves, medication timestamps, and notes.
  - 🐾 **`breed_detection_logs`**: MobileNetV2 ONNX deep-learning inferences, top-3 confidence rankings, and image metadata.
  - 🧠 **`recommendation_logs`**: Multi-target Random Forest diet formulas and wellness suggestions.
  - ⭐ **`reviews_feedback`**: Unstructured customer testimonials and feedback.

---

## 🚀 Setting Up MongoDB Atlas (Free M0 Cluster)

1. **Sign Up:** Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a free account.
2. **Create Cluster:**
   - Choose **M0 (Free)** tier.
   - Select cloud provider (AWS / Google Cloud) and region closest to your Render service (e.g. *AWS us-east-1* or *Oregon*).
3. **Database Access:**
   - Go to **Security** -> **Database Access**.
   - Click **Add New Database User**.
   - Username: `petcare_user`
   - Password: Choose a secure password (e.g., `PetCareMongo2026#`).
   - Role: **Built-in Role: Read and write to any database**.
4. **Network Access:**
   - Go to **Security** -> **Network Access**.
   - Click **Add IP Address**.
   - Select **Allow Access from Anywhere** (`0.0.0.0/0`) so Render and Vercel can connect.
5. **Get Connection String:**
   - In Atlas Dashboard, click **Connect** on your cluster.
   - Choose **Drivers** (Python).
   - Copy the URI, replacing `<password>` with your database password:
     ```
     mongodb+srv://petcare_user:PetCareMongo2026#@cluster0.xxxxx.mongodb.net/petcare_companion_db?retryWrites=true&w=majority
     ```

---

## ⚙️ Connecting to the Project

### On Render (Web Service):
In your Render Dashboard -> `petcare-backend` -> **Environment**:
- Add **`MONGODB_URI`** with your Atlas connection string.

### On Local Development:
Add to your `.env` file or export in terminal:
```bash
MONGODB_URI="mongodb+srv://petcare_user:PetCareMongo2026#@cluster0.xxxxx.mongodb.net/petcare_companion_db?retryWrites=true&w=majority"
```

---

## 🔄 Syncing Existing Records to MongoDB Atlas

Run the included synchronization management utility:
```bash
python manage.py sync_to_mongodb
```
This migrates your existing chat history, health logs, and recommendations into MongoDB Atlas automatically.

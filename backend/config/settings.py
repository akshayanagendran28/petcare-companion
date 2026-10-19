"""
Django settings for Pet Care Companion project.
Full-Stack AI-Powered Pet Care and Marketplace Platform.
"""

from pathlib import Path
import os
import sys

# Official Oracle Driver (python-oracledb) compatibility for Django Oracle Backend
try:
    import oracledb
    oracledb.version = "8.3.0"
    sys.modules["cx_Oracle"] = oracledb
except ImportError:
    pass

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent if BACKEND_DIR.name == 'backend' else BACKEND_DIR
BASE_DIR = PROJECT_ROOT

# Ensure backend and root are on sys.path
for p in [str(BACKEND_DIR), str(PROJECT_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-pet-care-companion-top-secret-key-2026-xyz')

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'corsheaders',
    'rest_framework',
    
    # Core Modular Apps
    'users.apps.UsersConfig',
    'pets.apps.PetsConfig',
    'marketplace.apps.MarketplaceConfig',
    'bookings.apps.BookingsConfig',
    'reviews.apps.ReviewsConfig',
    'adoption.apps.AdoptionConfig',
    'matchhub.apps.MatchhubConfig',
    'health.apps.HealthConfig',
    'notifications.apps.NotificationsConfig',
    'lostfound.apps.LostfoundConfig',
    'chatbot.apps.ChatbotConfig',
    'recommendations.apps.RecommendationsConfig',
    'breed_detection.apps.BreedDetectionConfig',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# CORS Configuration for Vercel Frontend & External Clients
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() in ('true', '1', 't')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/.*\.vercel\.app$",
    r"^https:\/\/.*\.onrender\.com$",
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://localhost',
    'http://0.0.0.0:8000',
    'https://*.onrender.com',
    'https://*.vercel.app',
    'https://*.railway.app',
    'https://*.pythonanywhere.com',
]

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_AGE = 86400

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATE_DIRS = [
    PROJECT_ROOT / 'frontend' / 'templates',
    PROJECT_ROOT / 'templates',
    BACKEND_DIR / 'templates',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [d for d in TEMPLATE_DIRS if d.exists()],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notification_badge',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# 1. Cloud PostgreSQL (when DATABASE_URL is set by Render)
# 2. Oracle Database (when USE_ORACLE=True)
# 3. Ephemeral / Runtime ORM Cache (database/app_cache.sqlite3) synchronized with MongoDB Atlas NoSQL
DATABASE_URL = os.getenv('DATABASE_URL')
USE_ORACLE = os.getenv('USE_ORACLE', 'False').lower() in ('true', '1', 't')

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True
            )
        }
    except Exception:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': PROJECT_ROOT / 'database' / 'app_cache.sqlite3',
            }
        }
elif USE_ORACLE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': os.getenv('ORACLE_DB_SERVICE_NAME', 'FREEPDB1'),
            'USER': os.getenv('ORACLE_DB_USER', 'pet_care_user'),
            'PASSWORD': os.getenv('ORACLE_DB_PASSWORD', 'PetCare123#'),
            'HOST': os.getenv('ORACLE_DB_HOST', 'localhost'),
            'PORT': os.getenv('ORACLE_DB_PORT', '1521'),
            'OPTIONS': {
                'threaded': True,
            },
        }
    }
else:
    # Runtime ORM cache populated dynamically from MongoDB Atlas NoSQL cloud collections
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': PROJECT_ROOT / 'database' / 'app_cache.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
_STATIC_CANDIDATES = [
    PROJECT_ROOT / 'frontend' / 'static',
    PROJECT_ROOT / 'static',
    BACKEND_DIR / 'static',
]
STATICFILES_DIRS = [d for d in _STATIC_CANDIDATES if d.exists()]
STATIC_ROOT = PROJECT_ROOT / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

# Media files (User uploads, Pet Photos, QR Codes)
MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_ROOT / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Ollama LLM Configuration
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3:4b')

# Razorpay Payment Gateway Configuration (Test Mode by default)
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_51PetCareCompanion2026')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'Secr3tPetCareCompanionKey2026')
RAZORPAY_CURRENCY = 'INR'

# MongoDB Atlas / NoSQL Document Database Configuration
DEFAULT_MONGODB_URI = "mongodb://akshayanagendran2005_db_user:oxMWH1iGaDTGc1nu@ac-7vgw2rk-shard-00-00.cgw10vq.mongodb.net:27017,ac-7vgw2rk-shard-00-01.cgw10vq.mongodb.net:27017,ac-7vgw2rk-shard-00-02.cgw10vq.mongodb.net:27017/petcare_companion_db?ssl=true&replicaSet=atlas-syqx38-shard-0&authSource=admin"
MONGODB_URI = os.getenv('MONGODB_URI', os.getenv('MONGO_URL', DEFAULT_MONGODB_URI))
MONGODB_NAME = os.getenv('MONGODB_NAME', 'petcare_companion_db')



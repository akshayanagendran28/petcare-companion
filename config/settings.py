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

BASE_DIR = Path(__file__).resolve().parent.parent

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

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://localhost',
    'http://0.0.0.0:8000',
    'https://*.onrender.com',
    'https://*.railway.app',
    'https://*.pythonanywhere.com',
]

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_AGE = 86400

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notification_badge',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# Primary Database Architecture: Oracle Database (19c / 21c / 23ai / Oracle Free XE)
# Set USE_ORACLE=True to connect directly to Oracle Database instance
USE_ORACLE = os.getenv('USE_ORACLE', 'False').lower() in ('true', '1', 't')

if USE_ORACLE:
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
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (User uploads, Pet Photos, QR Codes)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Ollama LLM Configuration
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3:4b')

"""
Vercel Serverless Function Entrypoint for Pet Care Companion Frontend
Enables zero-config deployment on Vercel using @vercel/python WSGI runner.
"""
import os
import sys
from pathlib import Path

# Add directories to system path
CURRENT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = CURRENT_DIR.parent
PROJECT_ROOT = FRONTEND_DIR.parent if FRONTEND_DIR.name == 'frontend' else FRONTEND_DIR
BACKEND_DIR = PROJECT_ROOT / 'backend'

for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

# Vercel looks for the `app` export for WSGI applications
app = get_wsgi_application()

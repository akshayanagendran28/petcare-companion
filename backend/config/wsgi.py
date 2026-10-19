import os
import sys
from pathlib import Path

# Add backend directory and project root to Python search path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent if BACKEND_DIR.name == 'backend' else BACKEND_DIR

for p in [str(BACKEND_DIR), str(PROJECT_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application  # Alias for serverless platforms like Vercel / Render

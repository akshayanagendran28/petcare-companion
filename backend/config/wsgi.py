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

# Production safeguard: Ensure database tables exist and data is populated
try:
    from django.db import connection
    from django.core.management import call_command
    tables = connection.introspection.table_names()
    if 'USERS' not in tables or 'django_session' not in tables:
        call_command('migrate', interactive=False, verbosity=0)
        call_command('restore_from_mongodb', verbosity=0)
except Exception:
    pass

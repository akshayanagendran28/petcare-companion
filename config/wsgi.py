import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'

for p in [str(ROOT_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application

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

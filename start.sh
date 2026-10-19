#!/usr/bin/env bash
set -e

PORT="${PORT:-10000}"
echo "=========================================================="
echo "    Pet Care Companion - Launching on Port: ${PORT}       "
echo "=========================================================="

echo "===> Applying Database Migrations..."
python manage.py migrate --no-input

# Restore data from MongoDB in background so Gunicorn opens the port immediately!
echo "===> Triggering Background Data Sync from MongoDB Atlas..."
python manage.py restore_from_mongodb > /dev/null 2>&1 &

echo "===> Starting Gunicorn Server immediately on 0.0.0.0:${PORT}..."
exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - config.wsgi:application

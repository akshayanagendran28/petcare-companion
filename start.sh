#!/usr/bin/env bash
set -e

PORT="${PORT:-10000}"
echo "=========================================================="
echo "    Pet Care Companion - Launching on Port: ${PORT}       "
echo "=========================================================="

echo "===> Applying Database Migrations..."
python manage.py migrate --no-input

echo "===> Restoring Data from MongoDB Atlas..."
python manage.py restore_from_mongodb || echo "[WARN] restore_from_mongodb skipped or completed"

echo "===> Syncing Collections to MongoDB Atlas..."
python manage.py sync_to_mongodb || echo "[WARN] sync_to_mongodb skipped or completed"

echo "===> Starting Gunicorn Server bound to 0.0.0.0:${PORT}..."
exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 --access-logfile - --error-logfile - config.wsgi:application

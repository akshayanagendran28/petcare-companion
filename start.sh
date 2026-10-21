#!/usr/bin/env bash
set -e

PORT="${PORT:-10000}"
echo "=========================================================="
echo "    Pet Care Companion - Launching on Port: ${PORT}       "
echo "=========================================================="

echo "===> Ensuring Database Schema & Tables..."
python manage.py migrate --no-input

echo "===> Restoring Data from MongoDB Atlas..."
python manage.py restore_from_mongodb || echo "[WARN] restore_from_mongodb completed with notice"

echo "===> Starting Gunicorn Server on 0.0.0.0:${PORT}..."
exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - config.wsgi:application

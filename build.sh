#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=========================================================="
echo "    Pet Care Companion - Render Deployment Build Hook    "
echo "=========================================================="

echo "===> Installing Python Dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
elif [ -f "backend/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r backend/requirements.txt
fi

echo "===> Collecting Static Assets..."
if [ -f "manage.py" ]; then
    python manage.py collectstatic --no-input
elif [ -f "backend/manage.py" ]; then
    python backend/manage.py collectstatic --no-input
fi

echo "===> Running Database Migrations on Render PostgreSQL / SQLite..."
if [ -f "manage.py" ]; then
    python manage.py migrate --no-input
elif [ -f "backend/manage.py" ]; then
    python backend/manage.py migrate --no-input
fi

echo "===> Build completed successfully!"

#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=========================================================="
echo "    Pet Care Companion - Render Deployment Build Hook    "
echo "=========================================================="

echo "===> Installing Python Dependencies..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
fi

echo "===> Collecting Static Assets..."
python manage.py collectstatic --no-input

echo "===> Applying Database Migrations & Initializing Schema..."
python manage.py migrate --no-input

echo "===> Restoring Collections from MongoDB Atlas..."
python manage.py restore_from_mongodb || echo "[WARN] restore_from_mongodb completed with notice"

echo "===> Build completed successfully!"

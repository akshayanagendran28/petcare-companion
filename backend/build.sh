#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=========================================================="
echo "    Pet Care Companion - Backend Render Build Hook       "
echo "=========================================================="

echo "===> Installing Python Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "===> Collecting Static Assets..."
python manage.py collectstatic --no-input

echo "===> Running Database Migrations on Render PostgreSQL..."
python manage.py migrate --no-input

echo "===> Build completed successfully!"

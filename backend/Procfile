web: python manage.py migrate --no-input && python manage.py seed_data && python manage.py sync_to_mongodb && gunicorn --bind 0.0.0.0:$PORT config.wsgi:application --log-file -

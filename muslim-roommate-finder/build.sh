#!/bin/bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create a simple test user (inline, no management command)
echo "Creating test user..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
print('Creating user...')
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
user.set_password('test123')
user.save()
print('✅ Created user: testuser / test123')
" 2>&1 || echo "User creation failed, you'll need to register manually"

# Run the server with Gunicorn, using the port Render provides
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}

#!/usr/bin/env python3
"""
Simple script to create a test admin user for production.
Run this manually if the management command fails.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile

def create_test_user():
    print("Creating test user...")
    
    # Create or get user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Set password
    user.set_password('test123')
    user.save()
    
    # Create profile
    profile, profile_created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'name': 'Test User',
            'age': 25,
            'gender': 'male',
            'city': 'New York, NY',
            'bio': 'Test account for debugging',
            'is_looking_for_room': True,
            'halal_kitchen': True,
            'prayer_friendly': True,
            'guests_allowed': True,
            'contact_email': 'test@example.com'
        }
    )
    
    print(f"✅ User created: testuser / test123")
    print(f"✅ Profile created: {profile.name}")

if __name__ == '__main__':
    create_test_user()

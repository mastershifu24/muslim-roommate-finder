#!/usr/bin/env python
"""Fix sample profile data - set proper gender and city for all profiles"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Profile

print("\n🔧 Fixing sample profile data...\n")

# Define proper data for each profile
profile_data = {
    'Abdullah Malik': {
        'gender': 'male',
        'city': 'Seattle',
        'state': 'WA',
        'age': 26,
        'is_looking_for_room': False,
        'only_eats_zabihah': False,
        'prayer_friendly': True,
        'guests_allowed': True,
        'bio': 'Software developer at tech company. Have a room in my apartment near downtown.',
    },
    'Sarah Khan': {
        'gender': 'female',
        'city': 'New York',
        'state': 'NY',
        'age': 27,
        'is_looking_for_room': False,
        'only_eats_zabihah': True,
        'prayer_friendly': True,
        'guests_allowed': True,
        'bio': 'Nurse with a spare room in Brooklyn. Looking for a respectful Muslim sister.',
    },
    'Omar Ibrahim': {
        'gender': 'male',
        'city': 'Chicago',
        'state': 'IL',
        'age': 28,
        'is_looking_for_room': False,
        'only_eats_zabihah': True,
        'prayer_friendly': True,
        'guests_allowed': True,
        'bio': 'Software engineer with a room to rent. Looking for respectful Muslim roommate.',
    },
    'Layla Ahmed': {
        'gender': 'female',
        'city': 'Boston',
        'state': 'MA',
        'age': 24,
        'is_looking_for_room': True,
        'only_eats_zabihah': True,
        'prayer_friendly': True,
        'guests_allowed': False,
        'bio': 'Graduate student looking for a peaceful, prayer-friendly environment.',
    },
    'Mohammed Ali': {
        'gender': 'male',
        'city': 'Miami',
        'state': 'FL',
        'age': 30,
        'is_looking_for_room': True,
        'only_eats_zabihah': True,
        'prayer_friendly': True,
        'guests_allowed': True,
        'bio': 'Business owner looking for affordable housing near the Islamic center.',
    },
}

fixed_count = 0

for name, data in profile_data.items():
    try:
        profile = Profile.objects.get(name=name)
        
        # Update fields
        for field, value in data.items():
            setattr(profile, field, value)
        
        profile.save()
        print(f"✅ Updated: {name} ({data['gender']}, {data['city']})")
        fixed_count += 1
        
    except Profile.DoesNotExist:
        print(f"⚠️  Profile not found: {name}")

print(f"\n🎉 Fixed {fixed_count} profiles!")
print("\n✨ All profiles now have:")
print("   - Gender set")
print("   - City set")
print("   - Age set")
print("   - Islamic preferences")
print("   - Bio")
print("\nVisit http://127.0.0.1:8000/profiles/ to see them!")


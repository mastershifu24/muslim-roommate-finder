#!/usr/bin/env python
"""Quick diagnostic script to check profile data"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Profile

print("\n" + "="*60)
print("📊 PROFILE DIAGNOSTIC")
print("="*60)

profiles = Profile.objects.all()
print(f"\n✅ Total Profiles: {profiles.count()}\n")

for p in profiles:
    print(f"👤 {p.name}")
    print(f"   Gender: {p.gender if p.gender else 'NOT SET ❌'}")
    print(f"   City: {p.city if p.city else 'NOT SET'}")
    print(f"   Photo: {'✅ YES' if p.profile_photo else '❌ NO'}")
    if p.profile_photo:
        print(f"   Photo Path: {p.profile_photo.name}")
    print(f"   Looking for room: {p.is_looking_for_room}")
    print()

print("="*60)
print("\n🔍 QUICK FIXES:\n")

missing_gender = Profile.objects.filter(gender__isnull=True) | Profile.objects.filter(gender='')
if missing_gender.exists():
    print(f"⚠️  {missing_gender.count()} profiles missing gender!")
    print("   Run: python manage.py shell")
    print("   Then fix with: Profile.objects.filter(name='Name').update(gender='male')")
else:
    print("✅ All profiles have gender set")

print("\n" + "="*60)


#!/usr/bin/env python
"""Check if media files are properly configured"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from core.models import Profile

print("\n" + "="*60)
print("🔍 MEDIA FILES DIAGNOSTIC")
print("="*60)

print(f"\n📁 Settings:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")

print(f"\n📸 Profile Photos:")
profiles_with_photos = Profile.objects.exclude(profile_photo='')
print(f"   Profiles with photos: {profiles_with_photos.count()}")

for p in profiles_with_photos:
    photo_path = os.path.join(settings.MEDIA_ROOT, p.profile_photo.name)
    exists = os.path.exists(photo_path)
    print(f"\n   👤 {p.name}")
    print(f"      DB Path: {p.profile_photo.name}")
    print(f"      Full Path: {photo_path}")
    print(f"      File Exists: {'✅ YES' if exists else '❌ NO'}")
    print(f"      URL would be: {settings.MEDIA_URL}{p.profile_photo.name}")

print("\n" + "="*60)
print("\n🧪 TEST URL:")
print(f"   Visit: http://127.0.0.1:8000{settings.MEDIA_URL}profile_photos/abdullah_malik_profile.jpg")
print("   If this shows an image, media serving works!")
print("\n" + "="*60)


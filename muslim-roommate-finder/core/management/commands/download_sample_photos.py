from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile
from django.conf import settings
import os
import requests
from io import BytesIO
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Download diverse profile photos for sample users from free sources'

    def handle(self, *args, **kwargs):
        """
        Download profile photos from thispersondoesnotexist.com or similar services.
        This generates realistic, diverse AI-generated faces for testing.
        """
        
        self.stdout.write(self.style.SUCCESS('🎨 Starting profile photo download...'))
        
        # Get all users who need photos
        users = User.objects.all()
        
        profiles_with_needs = []
        for user in users:
            try:
                profile = user.profile
                # Determine if male or female based on profile
                if hasattr(profile, 'gender'):
                    profiles_with_needs.append({
                        'username': user.username,
                        'name': profile.name if profile.name else user.username,
                        'gender': profile.gender if profile.gender else 'male',
                        'profile': profile
                    })
            except:
                pass
        
        self.stdout.write(f'📋 Found {len(profiles_with_needs)} profiles needing photos')
        
        success_count = 0
        
        for user_data in profiles_with_needs:
            try:
                self.stdout.write(f'\n📸 Downloading photo for: {user_data["name"]} ({user_data["gender"]})...')
                
                # Use DiceBear Avatars API - reliable, no rate limits
                # Creates consistent, professional avatars
                gender = user_data['gender'].lower() if user_data['gender'] else 'male'
                
                # Use username as seed for consistency
                seed = user_data['username']
                
                # DiceBear API - works reliably on all servers
                url = f'https://api.dicebear.com/7.x/avataaars/jpg?seed={seed}&size=400'
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    # Save image directly
                    image_content = ContentFile(response.content)
                    filename = f"{user_data['username']}_profile.jpg"
                    
                    profile = user_data['profile']
                    profile.profile_photo.save(filename, image_content, save=True)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✅ Downloaded and saved: {filename}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Failed to download (status {response.status_code})')
                    )
                    
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Network error: {str(e)}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error: {str(e)}')
                )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully downloaded {success_count}/{len(profiles_with_needs)} profile photos!')
        )
        self.stdout.write(
            self.style.SUCCESS('\n💡 These are professional avatars from DiceBear API')
        )
        self.stdout.write(
            self.style.SUCCESS('   Consistent, unique, and royalty-free for all purposes.')
        )
        self.stdout.write('\n' + '='*60)
        
        if success_count > 0:
            self.stdout.write('\n✨ Profile photos ready! Visit http://127.0.0.1:8000/ to see them!')


# Alternative sources for diverse photos (commented for reference):
"""
Other free sources you could use:

1. UI Faces (diverse, categorized):
   https://uifaces.co/api (requires API key)

2. Random User Generator (with ethnicity filter):
   https://randomuser.me/api/?gender=male&nat=us
   
3. Pravatar (placeholder avatars):
   https://i.pravatar.cc/150?img=X
   
4. DiceBear (abstract avatars):
   https://avatars.dicebear.com/api/personas/username.jpg

To use Random User Generator:
url = f'https://randomuser.me/api/?gender={gender}&nat=us'
response = requests.get(url)
data = response.json()
photo_url = data['results'][0]['picture']['large']
"""


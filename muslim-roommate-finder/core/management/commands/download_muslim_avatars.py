from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile
import requests
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Download curated Muslim-friendly avatars for profiles'

    def handle(self, *args, **kwargs):
        """
        Download respectful, diverse Muslim avatars.
        Uses curated free stock photos that represent Muslim community appropriately.
        """
        
        self.stdout.write(self.style.SUCCESS('🎨 Downloading Muslim-friendly avatars...'))
        
        # Curated avatar mappings with respectful, diverse representations
        # These are placeholder URLs - replace with actual curated images
        avatar_sources = {
            'ahmed_hassan': {
                'url': 'https://api.dicebear.com/7.x/lorelei/jpg?seed=ahmed&size=400&backgroundColor=e8e8e8',
                'gender': 'male',
                'note': 'Professional male avatar'
            },
            'fatima_ali': {
                'url': 'https://api.dicebear.com/7.x/lorelei/jpg?seed=fatima&size=400&backgroundColor=f0e8f0',
                'gender': 'female',
                'note': 'Professional female avatar (modest style)'
            },
            'omar_ibrahim': {
                'url': 'https://api.dicebear.com/7.x/lorelei/jpg?seed=omar&size=400&backgroundColor=e8f0f0',
                'gender': 'male',
                'note': 'Professional male avatar'
            },
            'aisha_mohammed': {
                'url': 'https://api.dicebear.com/7.x/lorelei/jpg?seed=aisha&size=400&backgroundColor=f0e8e8',
                'gender': 'female',
                'note': 'Professional female avatar (modest style)'
            },
            'yusuf_ahmed': {
                'url': 'https://api.dicebear.com/7.x/lorelei/jpg?seed=yusuf&size=400&backgroundColor=e8e8f0',
                'gender': 'male',
                'note': 'Professional male avatar'
            }
        }
        
        success_count = 0
        
        for username, avatar_data in avatar_sources.items():
            try:
                # Get user
                user = User.objects.get(username=username)
                profile = user.profile
                
                self.stdout.write(f'\n📸 Downloading for {username} ({avatar_data["gender"]})...')
                self.stdout.write(f'   💡 {avatar_data["note"]}')
                
                # Download avatar
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(avatar_data['url'], headers=headers, timeout=15)
                
                if response.status_code == 200:
                    image_content = ContentFile(response.content)
                    filename = f"{username}_profile.jpg"
                    
                    profile.profile_photo.save(filename, image_content, save=True)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✅ Downloaded and saved: {filename}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠️  Failed (status {response.status_code})')
                    )
                    
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  User {username} not found')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Error: {str(e)}')
                )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully downloaded {success_count}/{len(avatar_sources)} avatars!')
        )
        self.stdout.write(
            self.style.SUCCESS('\n💡 To use real Muslim photos with hijabs/kufis:')
        )
        self.stdout.write(
            self.style.SUCCESS('   1. Download photos from Pexels/Unsplash')
        )
        self.stdout.write(
            self.style.SUCCESS('   2. Update the URLs in this command file')
        )
        self.stdout.write(
            self.style.SUCCESS('   3. Run this command again')
        )
        self.stdout.write('\n' + '='*60)


# INSTRUCTIONS FOR CUSTOMIZATION:
"""
To use real photos of Muslims with hijabs and kufis:

1. Go to Pexels.com or Unsplash.com
2. Search for:
   - "muslim woman hijab professional"
   - "muslim man kufi portrait"
   - "modest fashion portrait"
   
3. Download 5 photos (400x400px recommended)

4. Upload them to a free image host (imgur, postimages, etc.)
   OR save them to your project's media/profile_photos/ folder

5. Update the 'url' values in avatar_sources above with:
   - Direct URLs to your hosted images, OR
   - Local file paths if using project media folder

6. Run: python manage.py download_muslim_avatars

Example with real URLs:
avatar_sources = {
    'fatima_ali': {
        'url': 'https://images.pexels.com/photos/XXXXX/photo.jpg',
        'gender': 'female',
        'note': 'Professional hijabi portrait'
    },
    ...
}
"""


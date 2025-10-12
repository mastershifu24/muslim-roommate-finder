from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile
import os


class Command(BaseCommand):
    help = 'Link existing profile photos to user profiles'

    def handle(self, *args, **kwargs):
        """
        Link profile photos to profiles based on username matching.
        Example: ahmed_hassan_profile.jpg → ahmed_hassan user
        """
        
        # Get all available profile photos
        from django.conf import settings
        import glob
        
        profile_photos_dir = os.path.join(settings.MEDIA_ROOT, 'profile_photos')
        available_photos = [
            os.path.basename(f) for f in glob.glob(os.path.join(profile_photos_dir, '*.jpg'))
        ]
        
        self.stdout.write(f'📁 Found {len(available_photos)} profile photos in media folder')
        
        # Map usernames to photo files (try to match by name similarity)
        photo_mappings = {
            'abdullah_malik': 'profile.jpg',  # Generic
            'sarah_khan': 'fatima_ali_profile.jpg',  # Use female photo
            'omar_ibrahim': 'omar_ibrahim_profile.jpg',
            'layla_ahmed': 'aisha_mohammed_profile.jpg',  # Female photo
            'mohammed_ali': 'ahmed_hassan_profile.jpg',  # Male photo
        }
        
        # Also try exact matches
        for user in User.objects.all():
            username = user.username
            # Try exact match first
            exact_match = f'{username}_profile.jpg'
            if exact_match in available_photos:
                photo_mappings[username] = exact_match
        
        updated_count = 0
        
        for username, photo_filename in photo_mappings.items():
            try:
                # Get user and their profile
                user = User.objects.get(username=username)
                profile = user.profile
                
                # Set photo path
                photo_path = f'profile_photos/{photo_filename}'
                
                # Check if file exists
                from django.conf import settings
                full_path = os.path.join(settings.MEDIA_ROOT, photo_path)
                
                if os.path.exists(full_path):
                    profile.profile_photo = photo_path
                    profile.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Linked photo for {username}: {photo_filename}')
                    )
                    updated_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Photo file not found: {photo_filename}')
                    )
                    
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  User not found: {username}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error for {username}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully linked {updated_count} profile photos!')
        )
        self.stdout.write(
            self.style.SUCCESS('Run the development server and check profiles!')
        )


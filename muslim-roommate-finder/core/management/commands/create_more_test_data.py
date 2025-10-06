from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Room, RoomImage, RoomType, Amenity
from django.core.files import File
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Create more test data with remaining images'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating more test data...'))
        
        # Create more users and rooms with remaining images
        users_data = [
            {
                'username': 'layla_ahmed',
                'email': 'layla.ahmed@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Layla Ahmed',
                    'age': 24,
                    'gender': 'female',
                    'city': 'Boston',
                    'state': 'MA',
                    'bio': 'Medical student looking for a quiet place to study. I prefer halal food and prayer-friendly environment.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'layla.ahmed@example.com'
                }
            },
            {
                'username': 'mohammed_ali',
                'email': 'mohammed.ali@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Mohammed Ali',
                    'age': 28,
                    'gender': 'male',
                    'city': 'Miami',
                    'state': 'FL',
                    'bio': 'Software engineer with a spare room. Looking for a respectful Muslim brother.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'mohammed.ali@example.com'
                }
            }
        ]
        
        # Create users and profiles
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'User already exists: {user.username}')
            
            # Update profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults=user_data['profile']
            )
            if not created:
                for key, value in user_data['profile'].items():
                    setattr(profile, key, value)
                profile.save()
                self.stdout.write(f'Updated profile: {profile.name}')
            else:
                self.stdout.write(f'Created profile: {profile.name}')
        
        # Create rooms with remaining images
        room_data = [
            {
                'title': 'Spacious Room in Boston - Sisters Only',
                'city': 'Boston',
                'price': 1100,
                'description': 'Beautiful room in a quiet neighborhood near medical school. Perfect for students.',
                'user': Profile.objects.get(user__username='layla_ahmed'),
                'images': ['room5.jpg', 'room6.jpg']
            },
            {
                'title': 'Modern Room in Miami - Brothers Only',
                'city': 'Miami',
                'price': 950,
                'description': 'Modern room in downtown Miami. Close to tech companies and masjid.',
                'user': Profile.objects.get(user__username='mohammed_ali'),
                'images': ['spacious-private-room-in-manhattan_room2.jpg', 'student-housing-near-asu_room3.jpg']
            }
        ]
        
        # Create rooms
        for room_info in room_data:
            room, created = Room.objects.get_or_create(
                title=room_info['title'],
                defaults={
                    'city': room_info['city'],
                    'price': room_info['price'],
                    'description': room_info['description'],
                    'user': room_info['user'],
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': room_info['user'].contact_email
                }
            )
            
            if created:
                self.stdout.write(f'Created room: {room.title}')
                
                # Add images to room
                room_images_dir = os.path.join(settings.MEDIA_ROOT, 'room_images')
                for i, image_file in enumerate(room_info['images']):
                    image_path = os.path.join(room_images_dir, image_file)
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            django_file = File(f, name=image_file)
                            room_image = RoomImage.objects.create(
                                room=room,
                                image=django_file,
                                is_primary=(i == 0),
                                caption=f"Room image {i + 1}"
                            )
                            self.stdout.write(f'Added image to room: {image_file}')
            else:
                self.stdout.write(f'Room already exists: {room.title}')
        
        self.stdout.write(self.style.SUCCESS('Test data creation completed!'))
        
        # Summary
        total_rooms = Room.objects.count()
        total_images = RoomImage.objects.count()
        total_profiles = Profile.objects.count()
        
        self.stdout.write(f'Total rooms: {total_rooms}')
        self.stdout.write(f'Total room images: {total_images}')
        self.stdout.write(f'Total profiles: {total_profiles}')

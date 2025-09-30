from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Room, RoomType, Amenity, RoomImage
from datetime import date, timedelta
import random
import os
from django.conf import settings
from django.core.files import File

class Command(BaseCommand):
    help = 'Create sample data for the Muslim Roommate Finder app'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Room Types
        room_types_data = [
            'Private Room',
            'Shared Room',
            'Master Bedroom',
            'Studio Apartment',
            'Entire Apartment'
        ]
        
        for room_type_name in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=room_type_name,
                defaults={'description': f'A {room_type_name.lower()} for rent'}
            )
            if created:
                self.stdout.write(f'Created room type: {room_type_name}')

        # Create Amenities
        amenities_data = [
            'WiFi',
            'Air Conditioning',
            'Heating',
            'Parking',
            'Laundry',
            'Kitchen Access',
            'Private Bathroom',
            'Shared Bathroom',
            'Furnished',
            'Unfurnished',
            'Pet Friendly',
            'No Smoking',
            'Gym Access',
            'Pool Access',
            'Balcony',
            'Garden Access'
        ]
        
        for amenity_name in amenities_data:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_name,
                defaults={'description': f'{amenity_name} available'}
            )
            if created:
                self.stdout.write(f'Created amenity: {amenity_name}')

        # Create Sample Users and Profiles
        sample_users_data = [
            {
                'username': 'ahmed_hassan',
                'email': 'ahmed.hassan@example.com',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'profile': {
                    'name': 'Ahmed Hassan',
                    'age': 25,
                    'gender': 'male',
                    'city': 'New York',
                    'is_looking_for_room': True,
                    'halal_kitchen': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'bio': 'Software engineer looking for a halal-friendly roommate in NYC. I pray 5 times a day and prefer a clean, quiet environment.',
                    'contact_email': 'ahmed.hassan@example.com'
                }
            },
            {
                'username': 'fatima_ali',
                'email': 'fatima.ali@example.com',
                'first_name': 'Fatima',
                'last_name': 'Ali',
                'profile': {
                    'name': 'Fatima Ali',
                    'age': 23,
                    'gender': 'female',
                    'city': 'Los Angeles',
                    'is_looking_for_room': False,
                    'halal_kitchen': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'bio': 'Medical student offering a room in my apartment. Looking for a practicing Muslim sister who values cleanliness and quiet study time.',
                    'contact_email': 'fatima.ali@example.com'
                }
            },
            {
                'username': 'omar_ibrahim',
                'email': 'omar.ibrahim@example.com',
                'first_name': 'Omar',
                'last_name': 'Ibrahim',
                'profile': {
                    'name': 'Omar Ibrahim',
                    'age': 28,
                    'gender': 'male',
                    'city': 'Chicago',
                    'is_looking_for_room': True,
                    'halal_kitchen': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'bio': 'Marketing professional seeking a roommate in Chicago. I enjoy cooking halal meals and would love to share a kitchen with someone who has similar values.',
                    'contact_email': 'omar.ibrahim@example.com'
                }
            },
            {
                'username': 'aisha_mohammed',
                'email': 'aisha.mohammed@example.com',
                'first_name': 'Aisha',
                'last_name': 'Mohammed',
                'profile': {
                    'name': 'Aisha Mohammed',
                    'age': 26,
                    'gender': 'female',
                    'city': 'Houston',
                    'is_looking_for_room': False,
                    'halal_kitchen': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'bio': 'Teacher with a spare room in my house. Looking for a respectful Muslim sister who values family-like atmosphere.',
                    'contact_email': 'aisha.mohammed@example.com'
                }
            },
            {
                'username': 'yusuf_ahmed',
                'email': 'yusuf.ahmed@example.com',
                'first_name': 'Yusuf',
                'last_name': 'Ahmed',
                'profile': {
                    'name': 'Yusuf Ahmed',
                    'age': 24,
                    'gender': 'male',
                    'city': 'Phoenix',
                    'is_looking_for_room': True,
                    'halal_kitchen': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'bio': 'Graduate student at ASU looking for affordable housing with other Muslim students. I am quiet, clean, and respectful.',
                    'contact_email': 'yusuf.ahmed@example.com'
                }
            }
        ]

        for user_data in sample_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(f'Created user: {user_data["username"]}')
            
            # Create or update profile
            profile_data = user_data['profile']
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults=profile_data
            )
            
            if profile_created:
                self.stdout.write(f'Created profile: {profile_data["name"]}')
                
                # Assign stock photos as profile pictures
                static_images = [
                    'static/images/mufid-majnun-cILyecy7y_o-unsplash.jpg',
                    'static/images/rumman-amin-i1bfxi1cFBY-unsplash.jpg'
                ]
                
                # Use different images for different profiles
                if user_data['username'] in ['ahmed_hassan', 'omar_ibrahim', 'yusuf_ahmed']:
                    # Male profiles get one image
                    image_path = os.path.join(settings.BASE_DIR, 'static/images/mufid-majnun-cILyecy7y_o-unsplash.jpg')
                else:
                    # Female profiles get another image
                    image_path = os.path.join(settings.BASE_DIR, 'static/images/rumman-amin-i1bfxi1cFBY-unsplash.jpg')
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        profile.profile_photo.save(
                            f'{user_data["username"]}_profile.jpg',
                            File(f),
                            save=True
                        )
                    self.stdout.write(f'Assigned profile photo to {profile_data["name"]}')

        # Create Sample Rooms
        sample_rooms_data = [
            {
                'title': 'Spacious Private Room in Manhattan',
                'description': 'Beautiful private room in a 2-bedroom apartment in the heart of Manhattan. The room is fully furnished with a queen bed, desk, and closet. Shared kitchen and living room with one other Muslim roommate. Building has doorman, gym, and rooftop access. Very close to subway stations and halal restaurants. Perfect for young professionals.',
                'city': 'New York',
                'price': 1200,
                'available_from': date.today() + timedelta(days=30),
                'phone_number': '(555) 123-4567',
                'halal_kitchen': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'fatima.ali@example.com'
            },
            {
                'title': 'Affordable Room Near UCLA',
                'description': 'Clean and comfortable room in Westwood, walking distance to UCLA campus. Shared apartment with 2 other Muslim students. Kitchen is halal-only, and we have a designated prayer area. Parking space included. Great for students or young professionals. Quiet neighborhood with easy access to public transportation and shopping.',
                'city': 'Los Angeles',
                'price': 900,
                'available_from': date.today() + timedelta(days=15),
                'phone_number': '(555) 987-6543',
                'halal_kitchen': True,
                'prayer_friendly': True,
                'guests_allowed': False,
                'contact_email': 'fatima.ali@example.com'
            },
            {
                'title': 'Master Bedroom in Chicago Townhouse',
                'description': 'Large master bedroom with private bathroom in a beautiful townhouse in Lincoln Park. Shared common areas with one other Muslim professional. Full kitchen access, in-unit laundry, and small backyard. Close to the lake, parks, and multiple mosques. Perfect for someone who values space and privacy while maintaining a sense of community.',
                'city': 'Chicago',
                'price': 1100,
                'available_from': date.today() + timedelta(days=45),
                'phone_number': '(555) 456-7890',
                'halal_kitchen': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'aisha.mohammed@example.com'
            },
            {
                'title': 'Room in Family-Friendly House',
                'description': 'Comfortable room in a family home in Houston. Perfect for a Muslim sister who values a family atmosphere. Shared kitchen (halal-only), living room, and backyard. The house has a prayer room and is close to several mosques and halal markets. Ideal for someone who wants a home-like environment rather than just a place to sleep.',
                'city': 'Houston',
                'price': 750,
                'available_from': date.today() + timedelta(days=20),
                'phone_number': '(555) 234-5678',
                'halal_kitchen': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'aisha.mohammed@example.com'
            },
            {
                'title': 'Student Housing Near ASU',
                'description': 'Budget-friendly room perfect for students near Arizona State University campus. Shared apartment with 3 other Muslim students. Study-friendly environment with quiet hours enforced. Kitchen is halal-only and we often cook meals together. Close to campus, library, and student services. Great for building friendships and academic success.',
                'city': 'Phoenix',
                'price': 600,
                'available_from': date.today() + timedelta(days=10),
                'phone_number': '(555) 345-6789',
                'halal_kitchen': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'yusuf.ahmed@example.com'
            }
        ]

        # Get room types and amenities
        private_room = RoomType.objects.get(name='Private Room')
        master_bedroom = RoomType.objects.get(name='Master Bedroom')
        
        amenities = list(Amenity.objects.all())
        
        # Get users for room ownership
        users_with_rooms = ['fatima_ali', 'aisha_mohammed', 'yusuf.ahmed@example.com']
        
        for i, room_data in enumerate(sample_rooms_data):
            # Assign room to appropriate user
            if i < 2:
                user = User.objects.get(username='fatima_ali')
            elif i < 4:
                user = User.objects.get(username='aisha_mohammed')
            else:
                user = User.objects.get(username='yusuf_ahmed')
            
            room, created = Room.objects.get_or_create(
                title=room_data['title'],
                defaults={
                    **room_data,
                    'user': user.profile,
                    'room_type': master_bedroom if 'Master' in room_data['title'] else private_room,
                }
            )
            
            if created:
                # Add random amenities
                room_amenities = random.sample(amenities, random.randint(3, 6))
                room.amenities.set(room_amenities)
                room.save()
                
                # Assign room images
                room_image_files = [
                    'room1.jpg', 'room2.jpg', 'room3.jpg', 
                    'room4.jpg', 'room5.jpg', 'room6.jpg'
                ]
                
                # Assign 1-2 images per room
                num_images = random.randint(1, 2)
                selected_images = random.sample(room_image_files, num_images)
                
                for idx, image_file in enumerate(selected_images):
                    image_path = os.path.join(settings.MEDIA_ROOT, 'room_images', image_file)
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            room_image = RoomImage.objects.create(
                                room=room,
                                is_primary=(idx == 0)  # First image is primary
                            )
                            room_image.image.save(
                                f'{room.slug}_{image_file}',
                                File(f),
                                save=True
                            )
                        self.stdout.write(f'Added image {image_file} to room: {room_data["title"]}')
                
                self.stdout.write(f'Created room: {room_data["title"]}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('You can now log in with any of these users:')
        self.stdout.write('- ahmed_hassan / password123')
        self.stdout.write('- fatima_ali / password123') 
        self.stdout.write('- omar_ibrahim / password123')
        self.stdout.write('- aisha_mohammed / password123')
        self.stdout.write('- yusuf_ahmed / password123')

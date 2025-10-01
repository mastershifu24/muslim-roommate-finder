#!/usr/bin/env python3
"""
Management command to create sample data for production deployment.
This version doesn't require local image files.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Room, RoomType, Amenity
import random


class Command(BaseCommand):
    help = 'Create sample data for production (no images required)'

    def handle(self, *args, **options):
        self.stdout.write("Creating production sample data...")
        
        # Create room types
        room_types_data = [
            "Private Room",
            "Shared Room", 
            "Master Bedroom",
            "Studio Apartment"
        ]
        
        for room_type_name in room_types_data:
            room_type, created = RoomType.objects.get_or_create(name=room_type_name)
            if created:
                self.stdout.write(f"Created room type: {room_type_name}")
        
        # Create amenities
        amenities_data = [
            "WiFi", "Air Conditioning", "Heating", "Parking", "Laundry",
            "Kitchen Access", "Private Bathroom", "Shared Bathroom", 
            "Furnished", "Utilities Included", "Pet Friendly", "Gym Access"
        ]
        
        amenities = []
        for amenity_name in amenities_data:
            amenity, created = Amenity.objects.get_or_create(name=amenity_name)
            amenities.append(amenity)
            if created:
                self.stdout.write(f"Created amenity: {amenity_name}")
        
        # Create sample users and profiles
        users_data = [
            {
                'username': 'ahmed_hassan',
                'email': 'ahmed@example.com',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'profile': {
                    'name': 'Ahmed Hassan',
                    'age': 25,
                    'gender': 'male',
                    'city': 'New York, NY',
                    'bio': 'Graduate student looking for a quiet place to study. I pray 5 times a day and prefer halal food.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'ahmed@example.com'
                }
            },
            {
                'username': 'fatima_ali',
                'email': 'fatima@example.com', 
                'first_name': 'Fatima',
                'last_name': 'Ali',
                'profile': {
                    'name': 'Fatima Ali',
                    'age': 23,
                    'gender': 'female',
                    'city': 'Los Angeles, CA',
                    'bio': 'Medical student seeking a peaceful environment. I value cleanliness and Islamic values.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'fatima@example.com'
                }
            },
            {
                'username': 'omar_ibrahim',
                'email': 'omar@example.com',
                'first_name': 'Omar', 
                'last_name': 'Ibrahim',
                'profile': {
                    'name': 'Omar Ibrahim',
                    'age': 28,
                    'gender': 'male',
                    'city': 'Chicago, IL',
                    'bio': 'Software engineer with a room to rent. Looking for respectful Muslim roommate.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'omar@example.com'
                }
            },
            {
                'username': 'aisha_mohammed',
                'email': 'aisha@example.com',
                'first_name': 'Aisha',
                'last_name': 'Mohammed', 
                'profile': {
                    'name': 'Aisha Mohammed',
                    'age': 26,
                    'gender': 'female',
                    'city': 'Houston, TX',
                    'bio': 'Teacher looking for a sister to share apartment. I love cooking and reading Quran.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'aisha@example.com'
                }
            },
            {
                'username': 'yusuf_ahmed',
                'email': 'yusuf@example.com',
                'first_name': 'Yusuf',
                'last_name': 'Ahmed',
                'profile': {
                    'name': 'Yusuf Ahmed', 
                    'age': 24,
                    'gender': 'male',
                    'city': 'Phoenix, AZ',
                    'bio': 'Engineering student at ASU. Looking for affordable housing near campus.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': False,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'yusuf@example.com'
                }
            }
        ]
        
        # Create users and profiles
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            # Always set password (in case user exists but password is wrong)
            user.set_password('password123')
            user.save()
            
            if created:
                self.stdout.write(f"Created user: {user.username}")
            else:
                self.stdout.write(f"Updated password for user: {user.username}")
            
            # Create profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults=user_data['profile']
            )
            
            if profile_created:
                self.stdout.write(f"Created profile: {profile.name}")
            else:
                self.stdout.write(f"Profile already exists: {profile.name}")
        
        # Create sample rooms
        rooms_data = [
            {
                'title': 'Spacious Private Room in Manhattan',
                'description': 'Beautiful private room in a 3-bedroom apartment in Manhattan. Close to subway stations and Islamic centers. The apartment has a fully equipped kitchen where halal cooking is welcome. Looking for a respectful Muslim roommate who values cleanliness and Islamic principles.',
                'city': 'New York, NY',
                'price': 1200,
                'available_from': '2024-01-15',
                'phone_number': '+1-555-0101',
                'only_eats_zabihah': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'omar@example.com'
            },
            {
                'title': 'Affordable Room Near UCLA',
                'description': 'Cozy room available near UCLA campus. Perfect for students. The house has a designated prayer area and halal-only kitchen. All utilities included in rent. Walking distance to masjid and halal restaurants. Ideal for serious students.',
                'city': 'Los Angeles, CA', 
                'price': 800,
                'available_from': '2024-02-01',
                'phone_number': '+1-555-0102',
                'only_eats_zabihah': True,
                'prayer_friendly': True,
                'guests_allowed': False,
                'contact_email': 'fatima@example.com'
            },
            {
                'title': 'Master Bedroom in Chicago Townhouse',
                'description': 'Large master bedroom with private bathroom in a beautiful townhouse. The house has a spacious living area perfect for family gatherings. Halal kitchen and prayer-friendly environment. Looking for a mature Muslim professional or family.',
                'city': 'Chicago, IL',
                'price': 950,
                'available_from': '2024-01-01',
                'phone_number': '+1-555-0103', 
                'only_eats_zabihah': True,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'omar@example.com'
            },
            {
                'title': 'Room in Family-Friendly House',
                'description': 'Comfortable room in a family-oriented house in Houston. We maintain Islamic values and have regular Quran study sessions. The kitchen is halal-only and we have a small prayer room. Perfect for sisters looking for a supportive Islamic environment.',
                'city': 'Houston, TX',
                'price': 650,
                'available_from': '2024-03-01',
                'phone_number': '+1-555-0104',
                'only_eats_zabihah': True,
                'prayer_friendly': True,
                'guests_allowed': False,
                'contact_email': 'aisha@example.com'
            },
            {
                'title': 'Student Housing Near ASU',
                'description': 'Budget-friendly room perfect for ASU students. The house is close to campus and has good study areas. We respect prayer times and maintain a quiet environment during study hours. Halal cooking is welcome in the shared kitchen.',
                'city': 'Phoenix, AZ',
                'price': 575,
                'available_from': '2024-02-15',
                'phone_number': '+1-555-0105',
                'only_eats_zabihah': False,
                'prayer_friendly': True,
                'guests_allowed': True,
                'contact_email': 'yusuf@example.com'
            }
        ]
        
        # Get room types
        private_room = RoomType.objects.get(name="Private Room")
        master_bedroom = RoomType.objects.get(name="Master Bedroom")
        
        # Create rooms
        for i, room_data in enumerate(rooms_data):
            # Assign to different users
            if i == 0:
                user = User.objects.get(username='omar_ibrahim')
            elif i == 1:
                user = User.objects.get(username='fatima_ali')
            elif i == 2:
                user = User.objects.get(username='omar_ibrahim')
            elif i == 3:
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
                self.stdout.write(f"Created room: {room.title}")
        
        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully created production sample data!\n"
                "You can now log in with any of these users:\n"
                "- ahmed_hassan / password123\n"
                "- fatima_ali / password123\n" 
                "- omar_ibrahim / password123\n"
                "- aisha_mohammed / password123\n"
                "- yusuf_ahmed / password123\n"
            )
        )

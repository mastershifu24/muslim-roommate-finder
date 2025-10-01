"""
Management command to create test accounts for multiple cities with room listings.
Usage: python manage.py create_city_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Room


class Command(BaseCommand):
    help = 'Creates test accounts for multiple cities with room listings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating multi-city test accounts...')
        
        # Sample users data - diverse cities for testing
        users_data = [
            # NEW YORK
            {
                'username': 'ahmed_hassan',
                'email': 'ahmed@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Ahmed Hassan',
                    'age': 25,
                    'gender': 'male',
                    'city': 'New York',
                    'state': 'NY',
                    'bio': 'Graduate student looking for a quiet place to study. I pray 5 times a day and prefer halal food.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'ahmed@example.com'
                }
            },
            {
                'username': 'sarah_nyc',
                'email': 'sarah.nyc@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Sarah Khan',
                    'age': 27,
                    'gender': 'female',
                    'city': 'New York',
                    'state': 'NY',
                    'bio': 'Nurse with a spare room in Brooklyn. Looking for a respectful Muslim sister.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'sarah.nyc@example.com'
                }
            },
            # LOS ANGELES
            {
                'username': 'fatima_ali',
                'email': 'fatima@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Fatima Ali',
                    'age': 23,
                    'gender': 'female',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'bio': 'Medical student seeking a peaceful environment. I value cleanliness and Islamic values.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'fatima@example.com'
                }
            },
            {
                'username': 'malik_la',
                'email': 'malik.la@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Malik Rahman',
                    'age': 30,
                    'gender': 'male',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'bio': 'Film producer with a large house in West LA. Have 2 rooms available.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'malik.la@example.com'
                }
            },
            # CHICAGO
            {
                'username': 'omar_ibrahim',
                'email': 'omar@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Omar Ibrahim',
                    'age': 28,
                    'gender': 'male',
                    'city': 'Chicago',
                    'state': 'IL',
                    'bio': 'Software engineer with a room to rent. Looking for respectful Muslim roommate.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'omar@example.com'
                }
            },
            {
                'username': 'zainab_chicago',
                'email': 'zainab.chi@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Zainab Ahmed',
                    'age': 24,
                    'gender': 'female',
                    'city': 'Chicago',
                    'state': 'IL',
                    'bio': 'Graduate student at Northwestern. Have a room available near campus.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'zainab.chi@example.com'
                }
            },
            # HOUSTON
            {
                'username': 'aisha_mohammed',
                'email': 'aisha@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Aisha Mohammed',
                    'age': 26,
                    'gender': 'female',
                    'city': 'Houston',
                    'state': 'TX',
                    'bio': 'Teacher looking for a sister to share apartment. I love cooking and reading Quran.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': False,
                    'contact_email': 'aisha@example.com'
                }
            },
            {
                'username': 'ibrahim_houston',
                'email': 'ibrahim.hou@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Ibrahim Yusuf',
                    'age': 32,
                    'gender': 'male',
                    'city': 'Houston',
                    'state': 'TX',
                    'bio': 'Engineer at an energy company. Have extra rooms in my house near the Masjid.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'ibrahim.hou@example.com'
                }
            },
            # PHOENIX
            {
                'username': 'yusuf_ahmed',
                'email': 'yusuf@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Yusuf Ahmed',
                    'age': 24,
                    'gender': 'male',
                    'city': 'Phoenix',
                    'state': 'AZ',
                    'bio': 'Engineering student at ASU. Looking for affordable housing near campus.',
                    'is_looking_for_room': True,
                    'only_eats_zabihah': False,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'yusuf@example.com'
                }
            },
            {
                'username': 'hassan_phoenix',
                'email': 'hassan.phx@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Hassan Ali',
                    'age': 29,
                    'gender': 'male',
                    'city': 'Phoenix',
                    'state': 'AZ',
                    'bio': 'Business owner with rooms near ASU campus. Great for students.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'hassan.phx@example.com'
                }
            },
            # DALLAS
            {
                'username': 'maryam_dallas',
                'email': 'maryam.dal@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Maryam Siddiqui',
                    'age': 28,
                    'gender': 'female',
                    'city': 'Dallas',
                    'state': 'TX',
                    'bio': 'Healthcare professional with a room available in Plano area.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': True,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'maryam.dal@example.com'
                }
            },
            # SEATTLE
            {
                'username': 'abdullah_seattle',
                'email': 'abdullah.sea@example.com',
                'password': 'password123',
                'profile': {
                    'name': 'Abdullah Malik',
                    'age': 26,
                    'gender': 'male',
                    'city': 'Seattle',
                    'state': 'WA',
                    'bio': 'Software developer at tech company. Have a room in my apartment near downtown.',
                    'is_looking_for_room': False,
                    'only_eats_zabihah': False,
                    'prayer_friendly': True,
                    'guests_allowed': True,
                    'contact_email': 'abdullah.sea@example.com'
                }
            },
        ]
        
        # Room listings for each city
        rooms_data = [
            # NEW YORK ROOMS
            {
                'username': 'sarah_nyc',
                'rooms': [
                    {
                        'title': 'Cozy Room in Brooklyn - Sisters Only',
                        'description': 'Spacious room in a 3-bedroom apartment in Brooklyn. Close to subway and halal restaurants. I work as a nurse and maintain a clean, quiet home. Perfect for a working professional or student. Prayer space available.',
                        'city': 'New York',
                        'price': 1200,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '212-555-0101'
                    },
                    {
                        'title': 'Affordable Room in Queens Near Masjid',
                        'description': 'Second room available in Queens, walking distance from the Islamic Center. Great neighborhood with many Muslim families. Utilities included in rent.',
                        'city': 'New York',
                        'price': 950,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': False,
                        'phone_number': '212-555-0102'
                    }
                ]
            },
            # LOS ANGELES ROOMS
            {
                'username': 'malik_la',
                'rooms': [
                    {
                        'title': 'Large Room in West LA House',
                        'description': 'Beautiful room with private bathroom in a large house in West LA. Close to UCLA and major tech companies. House has a prayer room and halal kitchen. Looking for a professional Muslim brother.',
                        'city': 'Los Angeles',
                        'price': 1400,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '310-555-0201'
                    },
                    {
                        'title': 'Room Near USC Campus',
                        'description': 'Second room available, perfect for USC students or young professionals. Quiet neighborhood, off-street parking, fast internet. Muslim household that values Islamic principles.',
                        'city': 'Los Angeles',
                        'price': 1100,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '310-555-0202'
                    }
                ]
            },
            # CHICAGO ROOMS
            {
                'username': 'omar_ibrahim',
                'rooms': [
                    {
                        'title': 'Modern Room in Downtown Chicago',
                        'description': 'Software engineer offering a room in my 2-bedroom apartment. Located in a quiet neighborhood with easy access to downtown Chicago. I value cleanliness and Islamic principles. Perfect for a working professional or graduate student.',
                        'city': 'Chicago',
                        'price': 900,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '312-555-0301'
                    }
                ]
            },
            {
                'username': 'zainab_chicago',
                'rooms': [
                    {
                        'title': 'Room Near Northwestern - Sisters Only',
                        'description': 'Room available near Northwestern campus in Evanston. Perfect for graduate students. I am also a grad student, so I understand the lifestyle. Quiet study environment, halal kitchen, and close to Masjid.',
                        'city': 'Chicago',
                        'price': 850,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': False,
                        'phone_number': '312-555-0302'
                    }
                ]
            },
            # HOUSTON ROOMS
            {
                'username': 'aisha_mohammed',
                'rooms': [
                    {
                        'title': "Sister's Room in Houston - Islamic Environment",
                        'description': 'Teacher offering a room for a Muslim sister in my apartment. I love cooking halal meals and reading Quran. Looking for someone who shares similar values and lifestyle. Very clean and peaceful environment.',
                        'city': 'Houston',
                        'price': 700,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': False,
                        'phone_number': '713-555-0401'
                    }
                ]
            },
            {
                'username': 'ibrahim_houston',
                'rooms': [
                    {
                        'title': 'Room in Houston Near Masjid - Brothers Only',
                        'description': 'Engineer offering rooms in my house located near the main Masjid in Houston. Great for professionals or students. House has dedicated prayer space and halal kitchen. Very peaceful Islamic environment.',
                        'city': 'Houston',
                        'price': 750,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '713-555-0402'
                    },
                    {
                        'title': 'Affordable Room in Houston Energy Corridor',
                        'description': 'Second room available in the energy corridor area. Perfect for professionals working in the energy industry. Clean, modern house with all amenities.',
                        'city': 'Houston',
                        'price': 650,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '713-555-0403'
                    }
                ]
            },
            # PHOENIX ROOMS
            {
                'username': 'hassan_phoenix',
                'rooms': [
                    {
                        'title': 'Student Room Near ASU Campus',
                        'description': 'Perfect for ASU students! Room available in a house walking distance from campus. Muslim household with prayer-friendly environment. Fast WiFi, quiet study space, and halal kitchen.',
                        'city': 'Phoenix',
                        'price': 600,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '480-555-0501'
                    },
                    {
                        'title': 'Affordable Room in Tempe',
                        'description': 'Another room available in Tempe area, close to ASU. Great for students or young professionals. Includes utilities and internet.',
                        'city': 'Phoenix',
                        'price': 550,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '480-555-0502'
                    }
                ]
            },
            # DALLAS ROOMS
            {
                'username': 'maryam_dallas',
                'rooms': [
                    {
                        'title': 'Room in Plano - Sisters Only',
                        'description': 'Healthcare professional offering a room in Plano area. Very clean and organized home. Close to shopping, restaurants, and Masjid. Perfect for working professional.',
                        'city': 'Dallas',
                        'price': 800,
                        'only_eats_zabihah': True,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '214-555-0601'
                    }
                ]
            },
            # SEATTLE ROOMS
            {
                'username': 'abdullah_seattle',
                'rooms': [
                    {
                        'title': 'Tech Professional Room in Seattle',
                        'description': 'Software developer offering a room in downtown Seattle apartment. Great for tech professionals working at Amazon, Microsoft, or other tech companies. Modern apartment with great amenities.',
                        'city': 'Seattle',
                        'price': 1100,
                        'only_eats_zabihah': False,
                        'prayer_friendly': True,
                        'guests_allowed': True,
                        'phone_number': '206-555-0701'
                    }
                ]
            },
        ]
        
        created_accounts = 0
        created_rooms = 0
        
        # Create users and profiles
        for user_data in users_data:
            # Create or get user
            user, user_created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            user.set_password(user_data['password'])
            user.save()
            
            # Create or update profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults=user_data['profile']
            )
            
            # If profile already existed, update it with the latest data
            if not profile_created:
                for key, value in user_data['profile'].items():
                    setattr(profile, key, value)
                profile.save()
            
            if user_created:
                created_accounts += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Created user: {user_data["username"]} ({user_data["profile"]["city"]})'
                ))
            else:
                self.stdout.write(f'  → Updated user: {user_data["username"]} ({user_data["profile"]["city"]})')
        
        # Create room listings
        for room_data in rooms_data:
            user = User.objects.get(username=room_data['username'])
            if hasattr(user, 'profile'):
                for room_info in room_data['rooms']:
                    # Check if room already exists
                    existing_room = Room.objects.filter(
                        user=user.profile,
                        title=room_info['title']
                    ).first()
                    
                    if not existing_room:
                        room = Room.objects.create(
                            user=user.profile,
                            title=room_info['title'],
                            description=room_info['description'],
                            city=room_info['city'],
                            price=room_info['price'],
                            is_active=True,
                            only_eats_zabihah=room_info['only_eats_zabihah'],
                            prayer_friendly=room_info['prayer_friendly'],
                            guests_allowed=room_info['guests_allowed'],
                            phone_number=room_info['phone_number']
                        )
                        created_rooms += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Created room: {room_info["title"]} in {room_info["city"]}'
                        ))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Total accounts: {len(users_data)}')
        self.stdout.write(f'Total rooms created: {created_rooms}')
        self.stdout.write('\n' + self.style.SUCCESS('Cities covered:'))
        cities = set(u['profile']['city'] for u in users_data)
        for city in sorted(cities):
            city_users = [u['username'] for u in users_data if u['profile']['city'] == city]
            self.stdout.write(f'  • {city}: {", ".join(city_users)}')
        
        self.stdout.write('\n' + self.style.WARNING('LOGIN INFO:'))
        self.stdout.write('  Username: (any of the usernames above)')
        self.stdout.write('  Password: password123')
        self.stdout.write(self.style.SUCCESS('\n✓ Multi-city test data created successfully!'))


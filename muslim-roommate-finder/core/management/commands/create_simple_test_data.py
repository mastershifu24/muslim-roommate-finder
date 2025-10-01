"""
Simple management command to create test accounts without allauth dependencies.
Usage: python manage.py create_simple_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Room


class Command(BaseCommand):
    help = 'Creates simple test accounts for multiple cities'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating simple test accounts...')
        
        # Simple test data
        test_accounts = [
            {
                'username': 'abdullah_malik',
                'email': 'abdullah.malik@example.com',
                'password': 'password123',
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
                'contact_email': 'abdullah.malik@example.com'
            },
            {
                'username': 'sarah_khan',
                'email': 'sarah.khan@example.com',
                'password': 'password123',
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
                'contact_email': 'sarah.khan@example.com'
            },
            {
                'username': 'omar_ibrahim',
                'email': 'omar@example.com',
                'password': 'password123',
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
        ]
        
        created_count = 0
        
        for account in test_accounts:
            # Create or get user
            user, user_created = User.objects.get_or_create(
                username=account['username'],
                defaults={'email': account['email']}
            )
            user.set_password(account['password'])
            user.save()
            
            # Create or update profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'name': account['name'],
                    'age': account['age'],
                    'gender': account['gender'],
                    'city': account['city'],
                    'state': account['state'],
                    'bio': account['bio'],
                    'is_looking_for_room': account['is_looking_for_room'],
                    'only_eats_zabihah': account['only_eats_zabihah'],
                    'prayer_friendly': account['prayer_friendly'],
                    'guests_allowed': account['guests_allowed'],
                    'contact_email': account['contact_email']
                }
            )
            
            if user_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Created user: {account["username"]} ({account["city"]})'
                ))
            else:
                self.stdout.write(f'  → Updated user: {account["username"]} ({account["city"]})')
        
        # Create some rooms
        room_data = [
            {
                'username': 'abdullah_malik',
                'title': 'Tech Professional Room in Seattle',
                'description': 'Software developer offering a room in downtown Seattle apartment. Great for tech professionals working at Amazon, Microsoft, or other tech companies. Modern apartment with great amenities.',
                'city': 'Seattle',
                'price': 1100,
                'only_eats_zabihah': False,
                'prayer_friendly': True,
                'guests_allowed': True,
                'phone_number': '206-555-0701'
            },
            {
                'username': 'sarah_khan',
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
                'username': 'omar_ibrahim',
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
        
        rooms_created = 0
        for room_info in room_data:
            user = User.objects.get(username=room_info['username'])
            if hasattr(user, 'profile'):
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
                    rooms_created += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Created room: {room_info["title"]} in {room_info["city"]}'
                    ))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Accounts created: {created_count}')
        self.stdout.write(f'Rooms created: {rooms_created}')
        self.stdout.write('\n' + self.style.WARNING('LOGIN INFO:'))
        self.stdout.write('  Username: abdullah_malik, sarah_khan, omar_ibrahim')
        self.stdout.write('  Password: password123')
        self.stdout.write(self.style.SUCCESS('\n✓ Simple test data created successfully!'))

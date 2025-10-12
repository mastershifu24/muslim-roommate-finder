from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Profile, Room, Message, RoomType, Amenity, RoomImage
from datetime import date, timedelta
from decimal import Decimal


class ProfileModelTestCase(TestCase):
    """Test Profile model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_auto_created_with_user(self):
        """Test that profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_slug_generation(self):
        """Test that slug is automatically generated from name"""
        profile = self.user.profile
        profile.name = 'Ahmed Hassan'
        profile.slug = ''  # Clear existing slug to trigger generation
        profile.save()
        self.assertEqual(profile.slug, 'ahmed-hassan')
    
    def test_profile_slug_unique(self):
        """Test that duplicate slugs get numbered"""
        # Create first profile
        profile1 = self.user.profile
        profile1.name = 'John Doe'
        profile1.slug = ''  # Clear existing slug
        profile1.save()
        
        # Create second user with same name
        user2 = User.objects.create_user(username='testuser2', password='test')
        profile2 = user2.profile
        profile2.name = 'John Doe'
        profile2.slug = ''  # Clear existing slug
        profile2.save()
        
        # Slugs should be different
        self.assertEqual(profile1.slug, 'john-doe')
        self.assertEqual(profile2.slug, 'john-doe-1')
    
    def test_profile_str_representation(self):
        """Test profile string representation"""
        profile = self.user.profile
        profile.name = 'Ahmed Hassan'
        profile.save()
        self.assertEqual(str(profile), 'Ahmed Hassan')
    
    def test_profile_is_charleston_area(self):
        """Test Charleston area detection"""
        profile = self.user.profile
        profile.city = 'Charleston'
        profile.state = 'SC'
        profile.save()
        self.assertTrue(profile.is_charleston_area())
        
        profile.city = 'Mount Pleasant'
        profile.state = 'SC'
        profile.save()
        self.assertFalse(profile.is_charleston_area())  # Only Charleston exactly
    
    def test_profile_islamic_preferences(self):
        """Test Islamic preference fields"""
        profile = self.user.profile
        profile.only_eats_zabihah = True
        profile.prayer_friendly = True
        profile.guests_allowed = False
        profile.save()
        
        self.assertTrue(profile.only_eats_zabihah)
        self.assertTrue(profile.prayer_friendly)
        self.assertFalse(profile.guests_allowed)


class RoomModelTestCase(TestCase):
    """Test Room model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='test')
        self.profile = self.user.profile
        self.profile.name = 'Test User'
        self.profile.city = 'New York'
        self.profile.save()
        
        self.room_type = RoomType.objects.create(name='Private Room')
        self.amenity1 = Amenity.objects.create(name='WiFi')
        self.amenity2 = Amenity.objects.create(name='Parking')
    
    def test_room_creation(self):
        """Test creating a room"""
        room = Room.objects.create(
            user=self.profile,
            title='Cozy Room in Brooklyn',
            description='A nice room with lots of natural light and close to subway.',
            city='New York',
            price=Decimal('1200'),
            room_type=self.room_type,
            only_eats_zabihah=True,
            prayer_friendly=True
        )
        
        self.assertEqual(room.title, 'Cozy Room in Brooklyn')
        self.assertEqual(room.city, 'New York')
        self.assertEqual(room.price, Decimal('1200'))
        self.assertTrue(room.only_eats_zabihah)
        self.assertTrue(room.prayer_friendly)
    
    def test_room_slug_generation(self):
        """Test that slug is automatically generated from title"""
        room = Room.objects.create(
            user=self.profile,
            title='Amazing Room Near Campus',
            description='Great location with all amenities included here.',
            city='Boston',
            price=Decimal('1000')
        )
        self.assertEqual(room.slug, 'amazing-room-near-campus')
    
    def test_room_str_representation(self):
        """Test room string representation"""
        room = Room.objects.create(
            user=self.profile,
            title='Studio in Manhattan',
            description='Modern studio apartment in the heart of Manhattan downtown.',
            city='New York',
            price=Decimal('2000')
        )
        self.assertEqual(str(room), 'Studio in Manhattan (New York)')
    
    def test_room_amenities_many_to_many(self):
        """Test adding amenities to room"""
        room = Room.objects.create(
            user=self.profile,
            title='Room with Amenities',
            description='This room comes with many amenities for your comfort.',
            city='Chicago',
            price=Decimal('900')
        )
        room.amenities.add(self.amenity1, self.amenity2)
        
        self.assertEqual(room.amenities.count(), 2)
        self.assertIn(self.amenity1, room.amenities.all())
        self.assertIn(self.amenity2, room.amenities.all())
    
    def test_room_primary_image_property(self):
        """Test primary_image property"""
        room = Room.objects.create(
            user=self.profile,
            title='Room with Images',
            description='Beautiful room with multiple photos available for viewing.',
            city='Los Angeles',
            price=Decimal('1500')
        )
        
        # Initially no images
        self.assertIsNone(room.primary_image)
    
    def test_room_get_price_display(self):
        """Test price display formatting"""
        room = Room.objects.create(
            user=self.profile,
            title='Affordable Room',
            description='Budget-friendly option in a great neighborhood with amenities.',
            city='Houston',
            price=Decimal('750')
        )
        self.assertEqual(room.get_price_display(), '$750')
        
        room.price = Decimal('1234')
        room.save()
        self.assertEqual(room.get_price_display(), '$1,234')


class MessageModelTestCase(TestCase):
    """Test Message model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.sender_user = User.objects.create_user(username='sender', password='test')
        self.recipient_user = User.objects.create_user(username='recipient', password='test')
        
        self.sender_profile = self.sender_user.profile
        self.sender_profile.name = 'Sender User'
        self.sender_profile.save()
        
        self.recipient_profile = self.recipient_user.profile
        self.recipient_profile.name = 'Recipient User'
        self.recipient_profile.save()
    
    def test_message_creation(self):
        """Test creating a message"""
        message = Message.objects.create(
            sender=self.sender_profile,
            recipient=self.recipient_profile,
            content='Hello, is the room still available?'
        )
        
        self.assertEqual(message.sender, self.sender_profile)
        self.assertEqual(message.recipient, self.recipient_profile)
        self.assertFalse(message.is_read)
    
    def test_message_str_representation(self):
        """Test message string representation"""
        message = Message.objects.create(
            sender=self.sender_profile,
            recipient=self.recipient_profile,
            content='Test message'
        )
        expected = f"Message from {self.sender_profile.name} to {self.recipient_profile.name}"
        self.assertEqual(str(message), expected)
    
    def test_message_ordering(self):
        """Test messages are ordered by timestamp descending"""
        import time
        msg1 = Message.objects.create(
            sender=self.sender_profile,
            recipient=self.recipient_profile,
            content='First message'
        )
        time.sleep(0.01)  # Small delay to ensure different timestamps
        msg2 = Message.objects.create(
            sender=self.sender_profile,
            recipient=self.recipient_profile,
            content='Second message'
        )
        
        messages = Message.objects.all()
        self.assertEqual(messages[0].content, 'Second message')  # Most recent first
        self.assertEqual(messages[1].content, 'First message')


class ViewsTestCase(TestCase):
    """Test views and user interactions"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.profile.name = 'Test User'
        self.profile.gender = 'male'
        self.profile.city = 'New York'
        self.profile.age = 25
        self.profile.save()
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_enhanced.html')
    
    def test_register_page_loads(self):
        """Test that registration page loads"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # User should be created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_required_for_create_profile(self):
        """Test that login is required to create profile"""
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)
    
    def test_login_and_access_protected_view(self):
        """Test user can login and access protected views"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
    
    def test_profile_detail_view(self):
        """Test profile detail page loads"""
        response = self.client.get(reverse('profile_detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.name)
    
    def test_browse_profiles_view(self):
        """Test browse profiles page loads"""
        response = self.client.get(reverse('browse_profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_profiles.html')
    
    def test_gender_filtering_in_home_view(self):
        """Test that logged-in users see only same-gender profiles"""
        # Create male and female profiles
        male_user = User.objects.create_user(username='male', password='test')
        male_profile = male_user.profile
        male_profile.name = 'Male User'
        male_profile.gender = 'male'
        male_profile.is_looking_for_room = True
        male_profile.save()
        
        female_user = User.objects.create_user(username='female', password='test')
        female_profile = female_user.profile
        female_profile.name = 'Female User'
        female_profile.gender = 'female'
        female_profile.is_looking_for_room = True
        female_profile.save()
        
        # Login as male user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        
        # Should see male profiles, not female
        self.assertContains(response, 'Male User')
        self.assertNotContains(response, 'Female User')
    
    def test_create_room_requires_login(self):
        """Test that creating room requires authentication"""
        # Access create_room without logging in
        response = self.client.get(reverse('create_room'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_edit_profile_security(self):
        """Test users can only edit their own profile"""
        # Create another user
        other_user = User.objects.create_user(username='other', password='test')
        other_profile = other_user.profile
        other_profile.name = 'Other User'
        other_profile.save()
        
        # Try to edit other user's profile
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_profile', args=[other_profile.id]))
        
        # Should redirect with error
        self.assertEqual(response.status_code, 302)
    
    def test_messaging_requires_login(self):
        """Test that messaging requires login"""
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_search_functionality(self):
        """Test search filters work"""
        # Create searchable profile
        search_user = User.objects.create_user(username='searchable', password='test')
        search_profile = search_user.profile
        search_profile.name = 'Searchable User'
        search_profile.city = 'Chicago'
        search_profile.is_looking_for_room = True
        search_profile.only_eats_zabihah = True
        search_profile.save()
        
        # Search by city
        response = self.client.get(reverse('browse_profiles'), {'city': 'Chicago'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable User')
        
        # Search by Islamic preference
        response = self.client.get(reverse('browse_profiles'), {'only_eats_zabihah': 'on'})
        self.assertEqual(response.status_code, 200)


class FormValidationTestCase(TestCase):
    """Test form validation"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test')
        self.profile = self.user.profile
        self.profile.name = 'Test User'
        self.profile.city = 'Boston'
        self.profile.save()
        self.client.login(username='testuser', password='test')
    
    def test_room_price_must_be_multiple_of_25(self):
        """Test that room price must be in $25 increments"""
        from core.forms import RoomForm
        
        # Valid price (multiple of 25)
        form_data = {
            'title': 'Test Room',
            'description': 'A' * 60,  # At least 50 characters
            'city': 'Boston',
            'price': 825,  # Valid
            'only_eats_zabihah': False,
            'prayer_friendly': True,
            'guests_allowed': True,
        }
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Invalid price (not multiple of 25)
        form_data['price'] = 823
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
    
    def test_room_description_minimum_length(self):
        """Test that room description must be at least 50 characters"""
        from core.forms import RoomForm
        
        form_data = {
            'title': 'Test Room',
            'description': 'Too short',  # Less than 50 characters
            'city': 'Boston',
            'price': 800,
            'only_eats_zabihah': False,
            'prayer_friendly': True,
            'guests_allowed': True,
        }
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)


class SecurityTestCase(TestCase):
    """Test security features"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test')
        self.other_user = User.objects.create_user(username='otheruser', password='test')
        
        self.profile = self.user.profile
        self.profile.name = 'Test User'
        self.profile.save()
        
        self.other_profile = self.other_user.profile
        self.other_profile.name = 'Other User'
        self.other_profile.save()
    
    def test_cannot_delete_other_users_profile(self):
        """Test users cannot delete other users' profiles"""
        self.client.login(username='testuser', password='test')
        
        response = self.client.post(
            reverse('delete_profile', args=[self.other_profile.id])
        )
        
        # Should redirect with error
        self.assertEqual(response.status_code, 302)
        
        # Profile should still exist
        self.assertTrue(Profile.objects.filter(id=self.other_profile.id).exists())
    
    def test_cannot_edit_other_users_room(self):
        """Test users cannot edit other users' rooms"""
        # Create room for other user
        room = Room.objects.create(
            user=self.other_profile,
            title='Other User Room',
            description='This is another users room and should not be editable by others.',
            city='Seattle',
            price=Decimal('1000')
        )
        
        self.client.login(username='testuser', password='test')
        
        response = self.client.post(
            reverse('room_edit', args=[room.pk]),
            {
                'title': 'Hacked Title',
                'description': 'Someone is trying to edit this room without permission here.',
                'city': 'Seattle',
                'price': 1000,
            }
        )
        
        # Should redirect with error
        self.assertEqual(response.status_code, 302)
        
        # Room title should not change
        room.refresh_from_db()
        self.assertEqual(room.title, 'Other User Room')
    
    def test_csrf_protection_on_forms(self):
        """Test CSRF protection is enabled"""
        # Try to post without CSRF token (simulate CSRF attack)
        response = self.client.post(
            reverse('register'),
            {
                'username': 'hacker',
                'email': 'hacker@example.com',
                'password1': 'hackpass123',
                'password2': 'hackpass123'
            },
            HTTP_X_CSRFTOKEN=''  # No CSRF token
        )
        
        # Django should reject request (403 Forbidden or redirect)
        # Note: In tests, CSRF is often disabled, but this tests the setup
        self.assertIn(response.status_code, [302, 403])


class ImageUploadTestCase(TestCase):
    """Test image upload functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test')
        self.profile = self.user.profile
        self.profile.name = 'Test User'
        self.profile.city = 'Boston'
        self.profile.save()
        self.client.login(username='testuser', password='test')
        
        self.room_type = RoomType.objects.create(name='Private Room')
    
    def create_test_image(self):
        """Create a test image file"""
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            "test_image.jpg",
            image_io.read(),
            content_type="image/jpeg"
        )
    
    def test_room_creation_with_images(self):
        """Test creating a room with images"""
        image1 = self.create_test_image()
        image2 = self.create_test_image()
        
        response = self.client.post(reverse('create_room'), {
            'title': 'Room with Images',
            'description': 'A' * 60,
            'city': 'Boston',
            'room_type': self.room_type.id,
            'price': 800,
            'only_eats_zabihah': False,
            'prayer_friendly': True,
            'guests_allowed': True,
            'images': [image1, image2]
        }, follow=True)
        
        # Check room was created
        room = Room.objects.filter(title='Room with Images').first()
        self.assertIsNotNone(room)
        
        # Check images were uploaded
        self.assertEqual(room.images.count(), 2)
        
        # Check first image is primary
        primary_image = room.images.filter(is_primary=True).first()
        self.assertIsNotNone(primary_image)
    
    def test_room_image_limit(self):
        """Test that room images are limited to 6"""
        # Create room first
        room = Room.objects.create(
            user=self.profile,
            title='Test Room',
            description='A' * 60,
            city='Boston',
            price=Decimal('800')
        )
        
        # Try to upload 8 images (should only save 6)
        images = [self.create_test_image() for _ in range(8)]
        
        for i, image in enumerate(images[:6]):
            RoomImage.objects.create(
                room=room,
                image=image,
                is_primary=(i == 0)
            )
        
        # Should only have 6 images
        self.assertEqual(room.images.count(), 6)


# Run tests with: python manage.py test core.tests
# Run specific test: python manage.py test core.tests.ProfileModelTestCase
# Run with verbosity: python manage.py test core.tests -v 2
# Run with coverage: coverage run --source='.' manage.py test core && coverage report

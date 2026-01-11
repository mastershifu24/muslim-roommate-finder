"""
Django REST Framework Serializers for Muslim Roommate Finder API
Converts Django models to JSON for mobile app consumption
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Room, RoomImage, Message, Amenity, RoomType, Feedback


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model with compatibility scores"""
    user = UserSerializer(read_only=True)
    whatsapp_link = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    compatibility_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'name', 'age', 'gender', 'city', 'state', 
            'neighborhood', 'profile_photo', 'profile_photo_url',
            'is_looking_for_room', 'only_eats_zabihah', 'prayer_friendly',
            'guests_allowed', 'bio', 'contact_email', 'whatsapp_number',
            'whatsapp_link', 'zip_code', 'created_at', 'updated_at',
            'compatibility_score'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()
    
    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
        return None
    
    def get_compatibility_score(self, obj):
        """Calculate compatibility with current user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                current_profile = request.user.profile
                return current_profile.calculate_compatibility_score(obj)
            except:
                return None
        return None


class RoomImageSerializer(serializers.ModelSerializer):
    """Serializer for Room Images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class AmenitySerializer(serializers.ModelSerializer):
    """Serializer for Amenities"""
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon', 'description']


class RoomTypeSerializer(serializers.ModelSerializer):
    """Serializer for Room Types"""
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description']


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    user = ProfileSerializer(read_only=True)
    images = RoomImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    room_type = RoomTypeSerializer(read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'user', 'title', 'description', 'room_type', 'amenities',
            'city', 'price', 'available_from', 'phone_number', 
            'only_eats_zabihah', 'prayer_friendly', 'guests_allowed',
            'contact_email', 'is_active', 'images', 'primary_image_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_primary_image_url(self, obj):
        primary = obj.primary_image
        if primary and primary.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary.image.url)
        return None


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Messages"""
    sender = ProfileSerializer(read_only=True)
    recipient = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'sender', 'timestamp']


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Feedback"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'name', 'email', 'feedback_type', 'priority',
            'title', 'message', 'page_url', 'browser_info', 'is_resolved',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_resolved', 'created_at']


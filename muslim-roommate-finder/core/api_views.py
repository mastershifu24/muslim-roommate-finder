"""
Django REST Framework API Views for Muslim Roommate Finder
Exposes all functionality as REST API endpoints for React Native app
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Profile, Room, RoomImage, Message, Amenity, RoomType, Feedback
from .serializers import (
    UserSerializer, UserRegistrationSerializer, ProfileSerializer,
    RoomSerializer, RoomImageSerializer, MessageSerializer,
    AmenitySerializer, RoomTypeSerializer, FeedbackSerializer
)


class UserRegistrationViewSet(viewsets.ViewSet):
    """Handle user registration"""
    permission_classes = [AllowAny]
    
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Profile CRUD operations
    Includes compatibility matching
    """
    queryset = Profile.objects.all().select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by gender (same as current user)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            user_gender = self.request.user.profile.gender
            if user_gender:
                queryset = queryset.filter(gender=user_gender)
        
        # Search filters
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(city__icontains=search) |
                Q(bio__icontains=search)
            )
        
        # Filter parameters
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        looking_for_room = self.request.query_params.get('looking_for_room', None)
        if looking_for_room:
            queryset = queryset.filter(is_looking_for_room=True)
        
        only_zabihah = self.request.query_params.get('only_zabihah', None)
        if only_zabihah:
            queryset = queryset.filter(only_eats_zabihah=True)
        
        prayer_friendly = self.request.query_params.get('prayer_friendly', None)
        if prayer_friendly:
            queryset = queryset.filter(prayer_friendly=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def matches(self, request):
        """Get top compatibility matches for current user"""
        try:
            current_profile = request.user.profile
            
            # Get all profiles looking for rooms (same gender)
            potential_matches = Profile.objects.filter(
                is_looking_for_room=True,
                gender=current_profile.gender
            ).exclude(id=current_profile.id)
            
            # Calculate compatibility scores
            matches = []
            for profile in potential_matches:
                score = current_profile.calculate_compatibility_score(profile)
                if score > 0:
                    matches.append({
                        'profile': profile,
                        'score': score
                    })
            
            # Sort by score (highest first)
            matches.sort(key=lambda x: x['score'], reverse=True)
            
            # Get top 20 matches
            top_matches = matches[:20]
            
            # Serialize profiles with scores
            result = []
            for match in top_matches:
                profile_data = ProfileSerializer(
                    match['profile'],
                    context={'request': request}
                ).data
                profile_data['compatibility_score'] = match['score']
                result.append(profile_data)
            
            return Response(result)
        
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Create a profile first to see matches'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        """Upload profile photo"""
        profile = self.get_object()
        
        # Check ownership
        if profile.user != request.user:
            return Response(
                {'error': 'You can only update your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if 'photo' not in request.FILES:
            return Response(
                {'error': 'No photo provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.profile_photo = request.FILES['photo']
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Room CRUD operations
    """
    queryset = Room.objects.filter(is_active=True).select_related('user').prefetch_related('images', 'amenities')
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by same gender as current user
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            user_gender = self.request.user.profile.gender
            if user_gender:
                queryset = queryset.filter(user__gender=user_gender)
        
        # Search filters
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search)
            )
        
        # Filter parameters
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        only_zabihah = self.request.query_params.get('only_zabihah', None)
        if only_zabihah:
            queryset = queryset.filter(only_eats_zabihah=True)
        
        prayer_friendly = self.request.query_params.get('prayer_friendly', None)
        if prayer_friendly:
            queryset = queryset.filter(prayer_friendly=True)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create room for current user's profile"""
        try:
            profile = self.request.user.profile
            serializer.save(user=profile)
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Create a profile first before listing a room')
    
    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        """Upload multiple images to a room"""
        room = self.get_object()
        
        # Check ownership
        if room.user.user != request.user:
            return Response(
                {'error': 'You can only add images to your own rooms'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        images = request.FILES.getlist('images')
        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit to 6 images total
        current_count = room.images.count()
        max_new = max(0, 6 - current_count)
        
        uploaded = []
        for i, image in enumerate(images[:max_new]):
            is_primary = (current_count == 0 and i == 0)
            room_image = RoomImage.objects.create(
                room=room,
                image=image,
                is_primary=is_primary
            )
            uploaded.append(RoomImageSerializer(room_image, context={'request': request}).data)
        
        return Response({
            'uploaded': len(uploaded),
            'images': uploaded
        })
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get current user's room listings"""
        try:
            profile = request.user.profile
            rooms = Room.objects.filter(user=profile)
            serializer = self.get_serializer(rooms, many=True)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response([])


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messaging
    """
    queryset = Message.objects.all().select_related('sender', 'recipient')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get messages where user is sender or recipient"""
        try:
            profile = self.request.user.profile
            return Message.objects.filter(
                Q(sender=profile) | Q(recipient=profile)
            ).order_by('-timestamp')
        except Profile.DoesNotExist:
            return Message.objects.none()
    
    def perform_create(self, serializer):
        """Send message from current user"""
        try:
            sender = self.request.user.profile
            serializer.save(sender=sender)
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Create a profile first before sending messages')
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get received messages"""
        try:
            profile = request.user.profile
            messages = Message.objects.filter(recipient=profile).order_by('-timestamp')
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response([])
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get sent messages"""
        try:
            profile = request.user.profile
            messages = Message.objects.filter(sender=profile).order_by('-timestamp')
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response([])
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        
        # Only recipient can mark as read
        if message.recipient.user != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for amenities (read-only)"""
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [AllowAny]


class RoomTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for room types (read-only)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]


class FeedbackViewSet(viewsets.ModelViewSet):
    """API endpoint for user feedback"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see their own feedback"""
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


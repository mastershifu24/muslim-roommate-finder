"""
API URLs for Muslim Roommate Finder React Native App
All endpoints prefixed with /api/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    UserRegistrationViewSet, ProfileViewSet, RoomViewSet,
    MessageViewSet, AmenityViewSet, RoomTypeViewSet, FeedbackViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'room-types', RoomTypeViewSet, basename='roomtype')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='api-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    
    # Include router URLs
    path('', include(router.urls)),
]


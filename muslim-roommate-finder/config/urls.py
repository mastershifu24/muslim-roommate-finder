from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth (keep existing for backward compatibility)
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Allauth URLs
    path('accounts/', include('allauth.urls')),

    # Dashboard & Listings
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-listings/', views.my_listings, name='my_listings'),

    # Profiles
    path('profiles/', views.browse_profiles, name='browse_profiles'),
    path('create/', views.create_profile, name='create_profile'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:profile_id>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:profile_id>/delete/', views.delete_profile, name='delete_profile'),
    path('profile/<int:profile_id>/contact/', views.contact_profile, name='contact_profile'),

    # Rooms
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path("rooms/<int:pk>/delete/", views.room_delete, name="room_delete"),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    
    # Messages
    path('inbox/', views.inbox, name='inbox'),
    path('compose/', views.compose_message, name='compose_message'),
    path('compose/<int:profile_id>/', views.compose_message, name='compose_message_to'),
    path('rooms/<int:room_id>/messages/', views.message_list_create, name='message_list_create'),
    path('rooms/<int:room_id>/messages/<int:pk>/', views.message_edit_delete, name='message_edit_delete'),
    
    # Debug endpoint
    path('create-test-account/', views.create_test_account, name='create_test_account'),
]

# Serve media files in both development and production
# Note: For production, consider using a CDN or cloud storage
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Profile, Room, Message, RoomType, Amenity
from .forms import ProfileForm, RoomForm, UserRegistrationForm, MessageForm


def home(request):
    """
    Enhanced home page with advanced filtering for rooms and profiles.
    Supports price ranges, location, age, gender, and Islamic preferences.
    """
    # Get filter parameters
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    gender_filter = request.GET.get('gender', '')
    preference_filter = request.GET.get('preference', '')
    
    # Age filters
    min_age = request.GET.get('min_age', '')
    max_age = request.GET.get('max_age', '')
    
    # Price filters (for rooms)
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Islamic preference filters
    only_eats_zabihah_filter = request.GET.get('only_eats_zabihah', '')
    prayer_friendly_filter = request.GET.get('prayer_friendly', '')
    guests_allowed_filter = request.GET.get('guests_allowed', '')

    # Filter Profiles - only show people looking for rooms by default
    profiles = Profile.objects.filter(is_looking_for_room=True)
    
    # Exclude current user's profile if logged in
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profiles = profiles.exclude(id=request.user.profile.id)
        
        # Filter by same gender for appropriate roommate matching
        user_gender = request.user.profile.gender
        profiles = profiles.filter(gender=user_gender)

    if search_query:
        profiles = profiles.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(bio__icontains=search_query)
        )

    if city_filter:
        profiles = profiles.filter(city__icontains=city_filter)
    if gender_filter:
        profiles = profiles.filter(gender=gender_filter)
    if preference_filter:
        # Map preference filters to Profile fields
        pref_map = {
            'only_eats_zabihah': 'only_eats_zabihah',
            'prayer_friendly': 'prayer_friendly',
            'guests_allowed': 'guests_allowed',
            'looking_for_room': 'is_looking_for_room',
            'offering_room': 'is_looking_for_room'
        }
        field = pref_map.get(preference_filter)
        if field:
            if preference_filter == 'looking_for_room':
                profiles = profiles.filter(is_looking_for_room=True)
            elif preference_filter == 'offering_room':
                # Show people offering rooms (not looking for rooms)
                profiles = Profile.objects.filter(is_looking_for_room=False)
            else:
                profiles = profiles.filter(**{field: True})

    # Filter Rooms
    available_rooms = Room.objects.filter(is_active=True)
    if search_query:
        available_rooms = available_rooms.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    if city_filter:
        available_rooms = available_rooms.filter(city__icontains=city_filter)
    if preference_filter in ['only_eats_zabihah', 'prayer_friendly', 'guests_allowed']:
        available_rooms = available_rooms.filter(**{preference_filter: True})

    # Unique cities for filter dropdowns
    cities = Profile.objects.values_list('city', flat=True).distinct().order_by('city')

    context = {
        'profiles': profiles,
        'available_rooms': available_rooms,
        'cities': cities,
        'search_query': search_query,
        'city_filter': city_filter,
        'gender_filter': gender_filter,
        'preference_filter': preference_filter,
        'profile_count': profiles.count(),
        'rooms_count': available_rooms.count(),
    }

    # Add enhanced filter context
    context.update({
        'min_price': min_price,
        'max_price': max_price,
        'only_eats_zabihah_filter': only_eats_zabihah_filter,
        'prayer_friendly_filter': prayer_friendly_filter,
        'guests_allowed_filter': guests_allowed_filter,
        'total_matches': 42,  # Placeholder
    })

    return render(request, 'home_enhanced.html', context)


def browse_profiles(request):
    """
    Dedicated page for browsing all profiles with advanced filtering and pagination.
    """
    # Get filter parameters
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    state_filter = request.GET.get('state', '')
    gender_filter = request.GET.get('gender', '')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')
    looking_for = request.GET.get('looking_for', '')
    only_eats_zabihah = request.GET.get('only_eats_zabihah', '')
    prayer_friendly = request.GET.get('prayer_friendly', '')
    guests_allowed = request.GET.get('guests_allowed', '')
    sort_by = request.GET.get('sort', 'newest')
    
    # Start with all profiles
    profiles = Profile.objects.all()
    
    # Exclude current user's profile if logged in
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profiles = profiles.exclude(id=request.user.profile.id)
    
    # Apply filters
    if search_query:
        profiles = profiles.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(neighborhood__icontains=search_query)
        )
    
    if city_filter:
        profiles = profiles.filter(city__icontains=city_filter)
    
    if state_filter:
        profiles = profiles.filter(state__icontains=state_filter)
    
    if gender_filter:
        profiles = profiles.filter(gender=gender_filter)
    
    if age_min:
        try:
            profiles = profiles.filter(age__gte=int(age_min))
        except ValueError:
            pass
    
    if age_max:
        try:
            profiles = profiles.filter(age__lte=int(age_max))
        except ValueError:
            pass
    
    if looking_for:
        if looking_for == 'room':
            profiles = profiles.filter(is_looking_for_room=True)
        elif looking_for == 'roommate':
            profiles = profiles.filter(is_looking_for_room=False)
        # 'both' shows all profiles
    
    if only_eats_zabihah:
        profiles = profiles.filter(only_eats_zabihah=True)
    
    if prayer_friendly:
        profiles = profiles.filter(prayer_friendly=True)
    
    if guests_allowed:
        profiles = profiles.filter(guests_allowed=True)
    
    # Apply sorting
    if sort_by == 'newest':
        profiles = profiles.order_by('-created_at')
    elif sort_by == 'oldest':
        profiles = profiles.order_by('created_at')
    elif sort_by == 'name':
        profiles = profiles.order_by('name')
    elif sort_by == 'age_youngest':
        profiles = profiles.order_by('age')
    elif sort_by == 'age_oldest':
        profiles = profiles.order_by('-age')
    else:
        profiles = profiles.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(profiles, 12)  # Show 12 profiles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique values for filter dropdowns
    cities = Profile.objects.values_list('city', flat=True).distinct().order_by('city')
    states = Profile.objects.values_list('state', flat=True).distinct().order_by('state')
    
    context = {
        'page_obj': page_obj,
        'profiles': page_obj,
        'cities': cities,
        'states': states,
        'search_query': search_query,
        'city_filter': city_filter,
        'state_filter': state_filter,
        'gender_filter': gender_filter,
        'age_min': age_min,
        'age_max': age_max,
        'looking_for': looking_for,
        'only_eats_zabihah': only_eats_zabihah,
        'prayer_friendly': prayer_friendly,
        'guests_allowed': guests_allowed,
        'sort_by': sort_by,
        'total_profiles': paginator.count,
    }
    
    return render(request, 'browse_profiles.html', context)


def profile_detail(request, profile_id):
    """
    Display a single profile with similar profile suggestions.
    """
    profile = get_object_or_404(Profile, id=profile_id)

    # Similar profiles: same city -> Charleston metro
    similar_profiles_list = []
    similar_profiles = Profile.objects.exclude(id=profile.id)

    if len(similar_profiles_list) < 3:
        city_matches = similar_profiles.filter(city=profile.city).exclude(
            id__in=[p.id for p in similar_profiles_list]
        )[:3-len(similar_profiles_list)]
        similar_profiles_list.extend(city_matches)

    if len(similar_profiles_list) < 3 and profile.is_charleston_area():
        charleston_cities = ['charleston', 'mount pleasant', 'west ashley']
        metro_matches = similar_profiles.filter(
            city__iregex=r'(' + '|'.join(charleston_cities) + ')'
        ).exclude(id__in=[p.id for p in similar_profiles_list])[:3-len(similar_profiles_list)]
        similar_profiles_list.extend(metro_matches)

    context = {
        'profile': profile,
        'similar_profiles': similar_profiles_list,
    }

    return render(request, 'profile_detail.html', context)



@login_required
def room_detail(request, pk):
    """
    Display a single room listing.
    """
    room = get_object_or_404(Room, pk=pk)
    return render(request, "room_detail.html", {"room": room})  # ✅ fixed


@login_required
def contact_profile(request, profile_id):
    """
    Contact a profile owner via messaging system.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    
    # Check if user has a profile
    try:
        sender_profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile before sending messages.')
        return redirect('create_profile')
    
    # Don't allow messaging yourself
    if profile == sender_profile:
        messages.error(request, 'You cannot send a message to yourself.')
        return redirect('profile_detail', profile_id=profile.id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender_profile
            message.recipient = profile
            message.save()
            messages.success(request, f'Your message has been sent to {profile.name}!')
            return redirect('profile_detail', profile_id=profile.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()

    return render(request, 'contact_profile.html', {'form': form, 'profile': profile})


@login_required
def create_profile(request):
    """
    Create a new profile or update existing one to prevent duplicates.
    """
    try:
        profile = Profile.objects.get(user=request.user)
        is_new = False
    except Profile.DoesNotExist:
        profile = None
        is_new = True

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            msg = 'Profile created successfully!' if is_new else 'Profile updated successfully!'
            messages.success(request, msg)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'create_profile.html', {'form': form})


@login_required
def edit_profile(request, profile_id):
    """
    Edit an existing profile - only allow users to edit their own profile.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    # Security check: only allow users to edit their own profile
    if profile.user != request.user:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('profile_detail', profile_id=profile.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_detail', profile_id=profile.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile, 'is_editing': True})


@login_required
def delete_profile(request, profile_id):
    """
    Delete a profile with confirmation - only allow users to delete their own profile.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    # Security check: only allow users to delete their own profile
    if profile.user != request.user:
        messages.error(request, 'You can only delete your own profile.')
        return redirect('profile_detail', profile_id=profile.id)

    if request.method == 'POST':
        profile_name = profile.name
        profile.delete()
        messages.success(request, f'Profile "{profile_name}" has been deleted successfully.')
        return redirect('home')

    return render(request, 'delete_profile.html', {'profile': profile})


@login_required
def create_room(request):
    """
    Create a room listing associated with the current user's profile.
    """
    # Check if user has a profile first
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile before listing a room.')
        return redirect('create_profile')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        form.fields['room_type'].queryset = RoomType.objects.order_by('name')
        form.fields['amenities'].queryset = Amenity.objects.order_by('name')
        if form.is_valid():
            room = form.save(commit=False)
            room.user = profile
            room.save()
            form.save_m2m()  # Save many-to-many relationships (amenities)
            messages.success(request, 'Room listing created successfully!')
            return redirect('room_detail', pk=room.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm()
        form.fields['room_type'].queryset = RoomType.objects.order_by('name')
        form.fields['amenities'].queryset = Amenity.objects.order_by('name')
    return render(request, 'create_room.html', {'form': form})


def register(request):
    """
    Register a new user and log them in immediately.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """
    User login view using Django AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    """
    Logout the current user.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """
    User dashboard showing their profile and recent room listings.
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')

    user_rooms = profile.rooms.all()[:5]

    return render(request, 'dashboard.html', {
        'rooms': user_rooms,
        'profiles': [profile],
    })


@login_required
def my_listings(request):
    """
    Show all room listings of the logged-in user.
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')

    user_rooms = Room.objects.filter(user=profile)
    return render(request, 'my_listings.html', {'rooms': user_rooms})


def advanced_search(request):
    """
    Advanced room search by rent, availability date, and room type.
    """
    min_rent = request.GET.get('min_rent', '')
    max_rent = request.GET.get('max_rent', '')
    available_date = request.GET.get('available', '')
    room_type = request.GET.get('room_type', '')
    amenities = request.GET.getlist('amenities')

    rooms = Room.objects.filter(is_active=True)

    if min_rent:
        rooms = rooms.filter(price__gte=min_rent)
    if max_rent:
        rooms = rooms.filter(price__lte=max_rent)
    if available_date:
        rooms = rooms.filter(available_from__lte=available_date)
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if amenities:
        rooms = rooms.filter(amenities__id__in=amenities).distinct()

    cities = Room.objects.values_list('city', flat=True).distinct().order_by('city')
    rent_ranges = [
        ('0-500', 'Under $500'),
        ('500-1000', '$500 - $1000'),
        ('1000-1500', '$1,000 - $1,500'),
        ('1500+', 'Over $1,500'),
    ]
    all_amenities = Amenity.objects.all().order_by('name')

    return render(request, 'advanced_search.html', {
        'rooms': rooms,
        'cities': cities,
        'rent_ranges': rent_ranges,
        'filters': request.GET,
        'amenities': all_amenities,
        'room_types': RoomType.objects.all(),
        'selected_amenities': amenities,
    })

@login_required
def room_edit(request, pk):
    """
    Edit a room listing - only allow the owner to edit their room.
    """
    room = get_object_or_404(Room, pk=pk)
    # Security check: only allow room owner to edit
    try:
        user_profile = request.user.profile
        if room.user != user_profile:
            messages.error(request, 'You can only edit your own room listings.')
            return redirect('room_detail', pk=room.pk)
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile first.')
        return redirect('create_profile')
    
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room listing updated successfully!')
            return redirect("room_detail", pk=room.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm(instance=room)
    return render(request, "room_edit.html", {"form": form, "room": room})

@login_required
def room_delete(request, pk):
    """
    Delete a room listing - only allow the owner to delete their room.
    """
    room = get_object_or_404(Room, pk=pk)
    # Security check: only allow room owner to delete
    try:
        user_profile = request.user.profile
        if room.user != user_profile:
            messages.error(request, 'You can only delete your own room listings.')
            return redirect('room_detail', pk=room.pk)
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile first.')
        return redirect('create_profile')
    if request.method == "POST":
        room_title = room.title
        room.delete()
        messages.success(request, f'Room listing "{room_title}" has been deleted successfully.')
        return redirect("dashboard")
    return render(request, "room_confirm_delete.html", {"room": room})


@login_required
def send_message(request, room_id=None):
    """
    Send a message to a user, optionally tied to a room.
    """
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        recipient = get_object_or_404(User, id=recipient_id)
        room = Room.objects.get(id=room_id) if room_id else None

        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            room=room,
            subject=subject,
            content=content
        )

        messages.success(request, 'Message sent successfully!')
        return redirect('inbox')

    room = Room.objects.get(id=room_id) if room_id else None
    return render(request, 'send_message.html', {'room': room})


@login_required
def inbox(request):
    """
    Inbox showing received and sent messages with better organization.
    Handle marking messages as read via POST request.
    """
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile first.')
        return redirect('create_profile')
    
    # Handle POST request to mark messages as read
    if request.method == 'POST':
        import json
        from django.http import JsonResponse
        try:
            data = json.loads(request.body)
            if data.get('action') == 'mark_read':
                # Mark all unread received messages as read
                Message.objects.filter(
                    recipient=user_profile, 
                    is_read=False
                ).update(is_read=True)
                return JsonResponse({'status': 'success'})
        except:
            pass
        return JsonResponse({'status': 'error'})
    
    received_messages = Message.objects.filter(recipient=user_profile).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=user_profile).order_by('-timestamp')

    return render(request, 'inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })


@login_required
def compose_message(request, profile_id=None):
    """
    Standalone compose message view - can be used to message any profile.
    """
    try:
        sender_profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'You need to create a profile before sending messages.')
        return redirect('create_profile')
    
    # If profile_id is provided, pre-select the recipient
    recipient_profile = None
    if profile_id:
        recipient_profile = get_object_or_404(Profile, id=profile_id)
        # Don't allow messaging yourself
        if recipient_profile == sender_profile:
            messages.error(request, 'You cannot send a message to yourself.')
            return redirect('inbox')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        recipient_id = request.POST.get('recipient_id')
        
        if form.is_valid() and recipient_id:
            recipient = get_object_or_404(Profile, id=recipient_id)
            message = form.save(commit=False)
            message.sender = sender_profile
            message.recipient = recipient
            message.save()
            messages.success(request, f'Your message has been sent to {recipient.name}!')
            return redirect('inbox')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()
    
    # Get all profiles except the current user's profile for recipient selection
    available_profiles = Profile.objects.exclude(user=request.user).order_by('name')
    
    return render(request, 'compose_message.html', {
        'form': form,
        'recipient_profile': recipient_profile,
        'available_profiles': available_profiles
    })


# -----------------------------
# New: Room Message CRUD Views
# -----------------------------

@login_required
def message_list_create(request, room_id):
    """
    List all messages in a room + create new ones.
    """
    room = get_object_or_404(Room, pk=room_id)
    messages_qs = Message.objects.filter(room=room)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.room = room
            msg.sender = request.user
            msg.save()
            return redirect('message_list_create', room_id=room.id)
    else:
        form = MessageForm()

    return render(request, 'messages/message_list.html', {
        'room': room,
        'messages': messages_qs,
        'form': form
    })


@login_required
def message_edit_delete(request, room_id, pk):
    """
    Edit or delete a specific message in a room.
    """
    room = get_object_or_404(Room, pk=room_id)
    message_obj = get_object_or_404(Message, pk=pk, room=room)

    if request.method == 'POST':
        if 'update' in request.POST:
            form = MessageForm(request.POST, instance=message_obj)
            if form.is_valid():
                form.save()
                return redirect('message_list_create', room_id=room.id)
        elif 'delete' in request.POST:
            message_obj.delete()
            return redirect('message_list_create', room_id=room.id)
    else:
        form = MessageForm(instance=message_obj)

    return render(request, 'messages/message_edit.html', {
        'room': room,
        'form': form,
        'message': message_obj
    })


def create_test_account(request):
    """
    Debug endpoint to create test accounts manually.
    Visit: /create-test-account/ to create all sample accounts
    """
    try:
        # Sample users data
        users_data = [
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
            }
        ]
        
        created_accounts = []
        
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
            
            created_accounts.append({
                'username': user_data['username'],
                'password': user_data['password'],
                'user_created': user_created,
                'profile_created': profile_created,
                'profile_updated': not profile_created
            })
        
        # Create sample room listings
        omar_user = User.objects.get(username='omar_ibrahim')
        if hasattr(omar_user, 'profile'):
            # Check if Omar already has rooms
            if not Room.objects.filter(user=omar_user.profile).exists():
                # Create a room for Omar
                Room.objects.create(
                    user=omar_user.profile,
                    title="Shared Apartment in Chicago - Muslim Friendly",
                    description="Software engineer offering a room in my 2-bedroom apartment. Located in a quiet neighborhood with easy access to downtown Chicago. I value cleanliness and Islamic principles. Perfect for a working professional or graduate student.",
                    city="Chicago, IL",
                    price=800,
                    is_active=True,
                    only_eats_zabihah=True,
                    prayer_friendly=True,
                    guests_allowed=True,
                    phone_number="312-555-0123"
                )
        
        # Create a room for Aisha
        aisha_user = User.objects.get(username='aisha_mohammed')
        if hasattr(aisha_user, 'profile'):
            # Check if Aisha already has this specific room
            if not Room.objects.filter(user=aisha_user.profile, title__contains="Sister's Room").exists():
                Room.objects.create(
                    user=aisha_user.profile,
                    title="Sister's Room in Houston - Islamic Environment",
                    description="Teacher offering a room for a Muslim sister in my apartment. I love cooking halal meals and reading Quran. Looking for someone who shares similar values and lifestyle. Very clean and peaceful environment.",
                    city="Houston, TX", 
                    price=650,
                    is_active=True,
                    only_eats_zabihah=True,
                    prayer_friendly=True,
                    guests_allowed=False,
                    phone_number="713-555-0456"
                )
        
        return JsonResponse({
            'success': True,
            'message': 'Sample accounts processed successfully! (Existing accounts updated with latest data)',
            'accounts': created_accounts,
            'login_info': [
                'ahmed_hassan / password123',
                'fatima_ali / password123', 
                'omar_ibrahim / password123',
                'aisha_mohammed / password123',
                'yusuf_ahmed / password123'
            ]
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
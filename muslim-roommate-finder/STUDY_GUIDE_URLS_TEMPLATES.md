# Study Guide: URLs & Templates - Complete Code Analysis (Updated 2025)

## 🎯 URLs and Templates Deep Dive

URLs route requests to views, and templates render the HTML that users see. This guide covers the URL patterns and template structure in your Muslim Roommate Finder app with recent enhancements including Django Allauth integration and improved UI.

---

## 🔗 URL Configuration (config/urls.py)

### **Main URL Configuration (All URLs in One File):**

```python
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
    
    # Allauth URLs (Social Authentication)
    path('accounts/', include('allauth.urls')),

    # Dashboard & Listings
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-listings/', views.my_listings, name='my_listings'),

    # Profiles
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
    
    # Messages
    path('inbox/', views.inbox, name='inbox'),
    path('rooms/<int:room_id>/messages/', views.message_list_create, name='message_list_create'),
    path('rooms/<int:room_id>/messages/<int:pk>/', views.message_edit_delete, name='message_edit_delete'),
]

# Media files serving (for development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### **Key Changes from Previous Version:**

1. **Single URLs File**: All URLs now in `config/urls.py` (no separate `core/urls.py`)
2. **Django Allauth Integration**: Social authentication at `/accounts/`
3. **Enhanced Room URLs**: Added edit and delete functionality
4. **Message System**: New messaging URLs for room-based conversations
5. **Media Files**: Static file serving configuration for images
6. **Parameter Consistency**: Mix of `profile_id`, `pk`, and `room_id` parameters

### **Key Concepts:**

1. **Path Patterns:** Define URL structure and parameters
2. **View Functions:** Connect URLs to view logic  
3. **Name Parameters:** Create named URLs for templates
4. **Integer Parameters:** Capture numeric IDs from URLs
5. **Include Patterns:** Django Allauth provides pre-built auth URLs
6. **Media Serving:** Development-only media file serving

---

## 🎨 Template System (Enhanced)

### **Template Structure:**

```
templates/
├── base.html                    # Enhanced base template with navbar
├── home.html                    # Main homepage (basic version)
├── home_enhanced.html           # Enhanced homepage with modern UI
├── profile_detail.html          # Individual profile view
├── contact_profile.html         # Contact form
├── delete_profile.html          # Delete confirmation
├── edit_profile.html            # Edit profile form
├── create_profile.html          # Create profile form
├── room_detail.html             # Individual room view
├── room_edit.html               # Edit room form
├── room_confirm_delete.html     # Room deletion confirmation
├── create_room.html             # Create room form
├── register.html                # User registration
├── login.html                   # User login
├── dashboard.html               # User dashboard
├── my_listings.html             # User's listings
├── inbox.html                   # Message inbox
├── advanced_search.html         # Advanced search page
├── messages/                    # Message templates
│   ├── message_edit.html        # Edit message
│   └── message_list.html        # Message list
└── partials/                    # Reusable components
    └── messages.html            # Flash messages partial
```

### **Key Template Enhancements:**

1. **Base Template**: Comprehensive navbar with responsive design
2. **Enhanced Home**: Modern UI with hero section, stats cards, and advanced filters
3. **Message System**: Dedicated templates for messaging functionality
4. **Partials**: Reusable components for better organization
5. **Responsive Design**: Mobile-first approach with Bootstrap 5
6. **Static Files**: Enhanced CSS and JavaScript integration

---

## 🏗️ Base Template (base.html) - Enhanced

**Purpose:** Provides consistent layout, navigation, and styling across all pages.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  {% load static %}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Muslim Roommate Finder{% endblock %}</title>

  <!-- Bootstrap -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

  <!-- Custom CSS -->
  <link href="{% static 'css/style.css' %}" rel="stylesheet">
  <link href="{% static 'css/enhanced.css' %}" rel="stylesheet">
</head>
<body class="container py-4">

  <!-- Header -->
  <header class="mb-4">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light rounded mb-3">
      <div class="container-fluid">
        <!-- Logo and Brand -->
        <a class="navbar-brand d-flex align-items-center" href="{% url 'home' %}">
          <img src="{% static 'images/logo.png' %}" alt="Logo" style="height:40px;" class="me-2">
          <span class="d-none d-md-inline">Muslim Roommate Finder</span>
          <span class="d-md-none">MRF</span>
        </a>
        
        <!-- Navigation items -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
              <a href="{% url 'dashboard' %}" class="nav-link btn btn-outline-primary btn-sm me-1 mb-1">Dashboard</a>
              <a href="{% url 'my_listings' %}" class="nav-link btn btn-outline-secondary btn-sm me-1 mb-1">My Listings</a>
              <a href="{% url 'inbox' %}" class="nav-link btn btn-outline-info btn-sm me-1 mb-1">Messages</a>
              <a href="{% url 'create_room' %}" class="nav-link btn btn-success btn-sm me-1 mb-1">+ List Room</a>
              {% if not user.profile %}
                <a href="{% url 'create_profile' %}" class="nav-link btn btn-warning btn-sm me-1 mb-1">+ Profile</a>
              {% endif %}
              <a href="{% url 'logout' %}" class="nav-link btn btn-outline-danger btn-sm mb-1">Logout</a>
            {% else %}
              <a href="{% url 'login' %}" class="nav-link btn btn-outline-primary btn-sm me-1 mb-1">Login</a>
              <a href="{% url 'register' %}" class="nav-link btn btn-primary btn-sm mb-1">Register</a>
            {% endif %}
          </div>
        </div>
      </div>
    </nav>

    <!-- Banner Block -->
    {% block banner %}
      <div>
        <img src="{% static 'images/banner.jpg' %}" alt="Banner" class="img-fluid rounded shadow">
      </div>
    {% endblock %}
  </header>

  <!-- Messages -->
  {% include "partials/messages.html" %}

  <!-- Page content -->
  {% block content %}{% endblock %}

  <!-- Footer -->
  <footer class="text-center py-4">
    {% block footer %}
      <p class="text-muted small mb-0">© {{ year|default:2025 }} Muslim Roommate Finder</p>
    {% endblock %}
  </footer>

  <!-- Scripts -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script src="{% static 'js/scripts.js' %}"></script>
</body>
</html>
```

### **Key Features:**

1. **Responsive Navbar**: Collapsible navigation with user-specific links
2. **Static Files Integration**: CSS and JavaScript loading
3. **Template Blocks**: Extensible sections for child templates
4. **Authentication Logic**: Different navigation for logged-in users
5. **Font Awesome Icons**: Icon support throughout the site
6. **Bootstrap 5**: Modern responsive framework
7. **Message System**: Flash messages integration

---

## 🏠 Enhanced Home Template (home_enhanced.html)

**Purpose:** Modern homepage with hero section, stats cards, advanced filters, and enhanced UI.

### **Key Features:**

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<!-- Hero Section -->
<div class="hero-section bg-gradient-primary text-white rounded-4 p-5 mb-5 text-center position-relative overflow-hidden">
  <div class="container position-relative">
    <h1 class="display-4 fw-bold mb-3">🏠 Find Your Perfect Muslim Roommate</h1>
    <p class="lead mb-4">Connect with fellow Muslims for halal-friendly housing solutions</p>
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- Quick Search Bar -->
        <form method="get" class="d-flex gap-2 mb-3">
          <input type="text" name="search" class="form-control form-control-lg shadow-sm" 
                 placeholder="🔍 Search by city, name, or description..." 
                 value="{{ search_query }}">
          <button type="submit" class="btn btn-light btn-lg px-4 shadow-sm">
            <i class="fas fa-search"></i>
          </button>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- Stats Cards -->
<div class="row mb-5">
  <div class="col-md-4 mb-3">
    <div class="card border-0 shadow-sm h-100 hover-lift">
      <div class="card-body text-center p-4">
        <div class="display-4 text-primary mb-3">🏠</div>
        <h3 class="card-title text-primary fw-bold">{{ rooms_count|default:0 }}</h3>
        <p class="card-text text-muted mb-0">Available Rooms</p>
      </div>
    </div>
  </div>
  <!-- More stats cards... -->
</div>

<!-- Advanced Filters Card -->
<div class="card border-0 shadow-sm mb-5">
  <div class="card-header bg-white border-0 py-3">
    <button class="btn btn-link text-decoration-none p-0 w-100 text-start fw-semibold fs-5" 
            type="button" data-bs-toggle="collapse" data-bs-target="#advancedFilters">
      <i class="fas fa-sliders-h me-2 text-primary"></i>Advanced Filters 
      <i class="fas fa-chevron-down float-end mt-1"></i>
    </button>
  </div>
  <div class="collapse" id="advancedFilters">
    <div class="card-body p-4">
      <form method="get" id="filterForm">
        <!-- Price Range Sliders -->
        <!-- Location Dropdowns -->
        <!-- Islamic Preferences Checkboxes -->
        <!-- Age Range Inputs -->
      </form>
    </div>
  </div>
</div>

<!-- Room and Profile Cards with Enhanced Styling -->
<!-- JavaScript for Interactive Features -->
{% endblock %}
```

### **Enhanced Features:**

1. **Hero Section**: Eye-catching gradient background with search
2. **Stats Cards**: Dynamic counters with hover effects
3. **Advanced Filters**: Collapsible filter panel with range sliders
4. **Interactive Elements**: JavaScript-powered price sliders and view toggles
5. **Responsive Design**: Mobile-first approach with breakpoints
6. **Modern UI**: Gradients, shadows, and smooth animations
7. **Islamic Theming**: Mosque icons and halal-friendly messaging

---

## 🎯 Template System Improvements

### **1. Template Inheritance:**
```html
<!-- base.html provides structure -->
{% extends "base.html" %}

<!-- Child templates add content -->
{% block content %}
  <!-- Page-specific content -->
{% endblock %}
```

### **2. Static Files Integration:**
```html
{% load static %}
<link href="{% static 'css/enhanced.css' %}" rel="stylesheet">
<script src="{% static 'js/scripts.js' %}"></script>
```

### **3. Template Tags & Filters:**
```html
<!-- URL generation -->
{% url 'room_detail' room.id %}

<!-- Conditional rendering -->
{% if user.is_authenticated %}
  <!-- Authenticated content -->
{% endif %}

<!-- Loops with empty handling -->
{% for room in available_rooms %}
  {{ room.title }}
{% empty %}
  No rooms available
{% endfor %}

<!-- Filters -->
{{ room.description|truncatewords:15 }}
{{ room.price|floatformat:0 }}
```

### **4. Modern CSS Features:**
- **CSS Grid & Flexbox**: Responsive layouts
- **CSS Custom Properties**: Theme variables
- **Animations**: Smooth transitions and hover effects
- **Media Queries**: Mobile-responsive breakpoints
<html>
<head>
    <title>Muslim Roommate Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .profile-card {
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }
        .profile-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body class="container py-4">
    <!-- Navigation Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Muslim Roommate Finder</h1>
        <div class="d-flex gap-2">
            {% if user.is_authenticated %}
                <a href="{% url 'dashboard' %}" class="btn btn-outline-primary">Dashboard</a>
                <a href="{% url 'my_listings' %}" class="btn btn-outline-secondary">My Listings</a>
                <a href="{% url 'logout' %}" class="btn btn-outline-danger">Logout</a>
            {% else %}
                <a href="{% url 'login' %}" class="btn btn-outline-primary">Login</a>
                <a href="{% url 'register' %}" class="btn btn-primary">Register</a>
            {% endif %}
            <a href="{% url 'create_room' %}" class="btn btn-success">+ List a Room</a>
            <a href="{% url 'create_profile' %}" class="btn btn-primary">+ Create Profile</a>
        </div>
    </div>

    <!-- Flash Messages -->
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}

    <!-- Quick Filter Buttons -->
    <div class="mb-3">
        <div class="btn-group" role="group">
            <a href="{% url 'home' %}" class="btn btn-outline-primary {% if not preference_filter %}active{% endif %}">
                Show All
            </a>
            <a href="?preference=offering_room" class="btn btn-outline-success {% if preference_filter == 'offering_room' %}active{% endif %}">
                🏠 Available Rooms
            </a>
            <a href="?preference=looking_for_room" class="btn btn-outline-info {% if preference_filter == 'looking_for_room' %}active{% endif %}">
                👥 Looking for Rooms
            </a>
        </div>
    </div>

    <!-- Search and Filter Form -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="get" class="row g-3">
                <!-- Search Box -->
                <div class="col-md-4">
                    <label for="search" class="form-label">Search</label>
                    <input type="text" class="form-control" id="search" name="search" 
                           value="{{ search_query }}" placeholder="Search by name, city, or bio...">
                </div>
                
                <!-- City Filter -->
                <div class="col-md-2">
                    <label for="city" class="form-label">City</label>
                    <select class="form-select" id="city" name="city">
                        <option value="">All Cities</option>
                        {% for city in cities %}
                            <option value="{{ city }}" {% if city_filter == city %}selected{% endif %}>
                                {{ city }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                
                <!-- Gender Filter -->
                <div class="col-md-2">
                    <label for="gender" class="form-label">Gender</label>
                    <select class="form-select" id="gender" name="gender">
                        <option value="">All Genders</option>
                        <option value="M" {% if gender_filter == 'M' %}selected{% endif %}>Male</option>
                        <option value="F" {% if gender_filter == 'F' %}selected{% endif %}>Female</option>
                    </select>
                </div>
                
                <!-- Preference Filter -->
                <div class="col-md-2">
                    <label for="preference" class="form-label">Preference</label>
                    <select class="form-select" id="preference" name="preference">
                        <option value="">All Preferences</option>
                        <option value="only_eats_zabihah" {% if preference_filter == 'only_eats_zabihah' %}selected{% endif %}>Only Eats Zabihah</option>
                        <option value="prayer_friendly" {% if preference_filter == 'prayer_friendly' %}selected{% endif %}>Prayer Friendly</option>
                        <option value="guests_allowed" {% if preference_filter == 'guests_allowed' %}selected{% endif %}>Guests Allowed</option>
                        <option value="looking_for_room" {% if preference_filter == 'looking_for_room' %}selected{% endif %}>Looking for Room</option>
                        <option value="offering_room" {% if preference_filter == 'offering_room' %}selected{% endif %}>Offering Room</option>
                    </select>
                </div>
                
                <!-- Search Button -->
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">Search</button>
                </div>
            </form>
            
            <!-- Clear Filters Link -->
            {% if search_query or city_filter or gender_filter or preference_filter %}
                <div class="mt-3">
                    <a href="{% url 'home' %}" class="btn btn-outline-secondary btn-sm">Clear All Filters</a>
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Available Rooms Section -->
    {% if available_rooms %}
        <div class="mb-4">
            <h3 class="text-success mb-3">
                🏠 Available Rooms ({{ rooms_count }})
            </h3>
            <div class="row">
                {% for room in available_rooms %}
                    <div class="col-md-4 mb-4">
                        <a href="{% url 'room_detail' room.id %}" class="text-decoration-none">
                            <div class="card h-100 profile-card border-success">
                                <div class="card-header bg-success text-white">
                                    <h5 class="card-title mb-0">{{ room.title }}</h5>
                                </div>
                                <div class="card-body">
                                    <h6 class="card-subtitle mb-2 text-muted">{{ room.city }}{% if room.neighborhood %} • {{ room.neighborhood }}{% endif %}</h6>
                                    {% if room.rent %}
                                        <p class="text-dark mb-2"><strong>Rent:</strong> ${{ room.rent }}</p>
                                    {% endif %}
                                    
                                    {% if room.description %}
                                        <p class="card-text text-dark">{{ room.description }}</p>
                                    {% endif %}
                                    
                                    <div class="mb-3">
                                        <small class="text-muted">
                                            <strong>Contact:</strong> {{ room.contact_email }}
                                        </small>
                                    </div>
                                    
                                    <div class="d-flex flex-wrap gap-1">
                                        {% if room.only_eats_zabihah %}
                                            <span class="badge bg-success">Only Eats Zabihah</span>
                                        {% endif %}
                                        {% if room.prayer_friendly %}
                                            <span class="badge bg-info">Prayer Friendly</span>
                                        {% endif %}
                                        {% if room.guests_allowed %}
                                            <span class="badge bg-warning">Guests Allowed</span>
                                        {% endif %}
                                        <span class="badge bg-success">Room Available</span>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endif %}

    <!-- People Looking for Rooms Section -->
    {% if profiles %}
        <div class="mb-4">
            <h3 class="text-primary mb-3">
                👥 People Looking for Rooms ({{ profile_count }})
            </h3>
            <div class="row">
                {% for profile in profiles %}
                    <div class="col-md-4 mb-4">
                        <a href="{{ profile.get_absolute_url }}" class="text-decoration-none">
                            <div class="card h-100 profile-card border-primary">
                                <div class="card-header bg-primary text-white">
                                    <h5 class="card-title mb-0">{{ profile.name }}, {{ profile.age }}</h5>
                                </div>
                                <div class="card-body">
                                    <h6 class="card-subtitle mb-2 text-muted">{{ profile.city }} | {{ profile.get_gender_display }}</h6>
                                    
                                    {% if profile.bio %}
                                        <p class="card-text text-dark">{{ profile.bio }}</p>
                                    {% endif %}
                                    
                                    <div class="mb-3">
                                        <small class="text-muted">
                                            <strong>Contact:</strong> {{ profile.contact_email }}
                                        </small>
                                    </div>
                                    
                                    <div class="d-flex flex-wrap gap-1">
                                        {% if profile.only_eats_zabihah %}
                                            <span class="badge bg-success">Only Eats Zabihah</span>
                                        {% endif %}
                                        {% if profile.prayer_friendly %}
                                            <span class="badge bg-info">Prayer Friendly</span>
                                        {% endif %}
                                        {% if profile.guests_allowed %}
                                            <span class="badge bg-warning">Guests Allowed</span>
                                        {% endif %}
                                        <span class="badge bg-primary">Looking for Room</span>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endif %}

    <!-- No Results Message -->
    {% if not profiles and not available_rooms %}
        <div class="text-center py-5">
            <h3 class="text-muted">No profiles or rooms found</h3>
            <p class="text-muted">
                {% if search_query or city_filter or gender_filter or preference_filter %}
                    Try adjusting your search criteria.
                {% else %}
                    Be the first to create a profile!
                {% endif %}
            </p>
            <a href="{% url 'create_profile' %}" class="btn btn-primary btn-lg">Create Your Profile</a>
        </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### **Key Template Concepts:**

1. **Template Tags:** `{% %}` for logic, `{{ }}` for variables
2. **Conditional Rendering:** `{% if %}` statements
3. **Loops:** `{% for %}` to iterate over lists
4. **URL Generation:** `{% url 'name' %}` for named URLs
5. **Bootstrap Classes:** Responsive design framework

---

## 👤 Profile Detail Template (profile_detail.html)

**Purpose:** Show detailed information about a specific profile.

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ profile.name }} - Muslim Roommate Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ profile.name }}, {{ profile.age }}</h1>
        <div class="d-flex gap-2">
            <a href="{% url 'home' %}" class="btn btn-outline-secondary">← Back to Home</a>
            <a href="{% url 'contact_profile' profile.id %}" class="btn btn-primary">Contact {{ profile.name }}</a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">About {{ profile.name }}</h5>
                    <p class="card-text">{{ profile.bio|default:"No bio provided." }}</p>
                    
                    <h6>Location</h6>
                    <p>{{ profile.city }}{% if profile.neighborhood %}, {{ profile.neighborhood }}{% endif %}</p>
                    
                    <h6>Contact Information</h6>
                    <p>Email: {{ profile.contact_email }}</p>
                    
                    <h6>Preferences</h6>
                    <div class="d-flex flex-wrap gap-2">
                        {% if profile.only_eats_zabihah %}
                            <span class="badge bg-success">Only Eats Zabihah</span>
                        {% endif %}
                        {% if profile.prayer_friendly %}
                            <span class="badge bg-info">Prayer Friendly</span>
                        {% endif %}
                        {% if profile.guests_allowed %}
                            <span class="badge bg-warning">Guests Allowed</span>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Similar Profiles</h5>
                </div>
                <div class="card-body">
                    {% if similar_profiles %}
                        {% for similar in similar_profiles %}
                            <div class="border-bottom pb-2 mb-2">
                                <h6><a href="{% url 'profile_detail' similar.id %}">{{ similar.name }}, {{ similar.age }}</a></h6>
                                <small class="text-muted">{{ similar.city }} • {{ similar.get_gender_display }}</small>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">No similar profiles found.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## 📝 Registration Template (register.html)

**Purpose:** User registration form.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Register - Muslim Roommate Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Create Account</h1>
                <a href="{% url 'home' %}" class="btn btn-outline-secondary">← Back to Home</a>
            </div>

            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}

            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">Username</label>
                            {{ form.username }}
                            {% if form.username.errors %}
                                <div class="text-danger">{{ form.username.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.email.id_for_label }}" class="form-label">Email</label>
                            {{ form.email }}
                            {% if form.email.errors %}
                                <div class="text-danger">{{ form.email.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.password1.id_for_label }}" class="form-label">Password</label>
                            {{ form.password1 }}
                            {% if form.password1.errors %}
                                <div class="text-danger">{{ form.password1.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.password2.id_for_label }}" class="form-label">Confirm Password</label>
                            {{ form.password2 }}
                            {% if form.password2.errors %}
                                <div class="text-danger">{{ form.password2.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Create Account</button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## 🔐 Login Template (login.html)

**Purpose:** User authentication form.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login - Muslim Roommate Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Login</h1>
                <a href="{% url 'home' %}" class="btn btn-outline-secondary">← Back to Home</a>
            </div>

            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}

            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">Username</label>
                            {{ form.username }}
                            {% if form.username.errors %}
                                <div class="text-danger">{{ form.username.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.password.id_for_label }}" class="form-label">Password</label>
                            {{ form.password }}
                            {% if form.password.errors %}
                                <div class="text-danger">{{ form.password.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Login</button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## 📊 Dashboard Template (dashboard.html)

**Purpose:** User's personal dashboard.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Muslim Roommate Finder</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Welcome, {{ user.username }}!</h1>
        <div class="d-flex gap-2">
            <a href="{% url 'my_listings' %}" class="btn btn-outline-primary">My Listings</a>
            <a href="{% url 'logout' %}" class="btn btn-outline-danger">Logout</a>
        </div>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}

    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">My Room Listings</h5>
                </div>
                <div class="card-body">
                    {% if rooms %}
                        {% for room in rooms %}
                            <div class="border-bottom pb-2 mb-2">
                                <h6><a href="{% url 'room_detail' room.id %}">{{ room.title }}</a></h6>
                                <small class="text-muted">{{ room.city }} • ${{ room.rent }}</small>
                            </div>
                        {% endfor %}
                        <a href="{% url 'my_listings' %}" class="btn btn-sm btn-outline-primary">View All</a>
                    {% else %}
                        <p class="text-muted">No room listings yet.</p>
                        <a href="{% url 'create_room' %}" class="btn btn-success">List a Room</a>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">My Profiles</h5>
                </div>
                <div class="card-body">
                    {% if profiles %}
                        {% for profile in profiles %}
                            <div class="border-bottom pb-2 mb-2">
                                <h6><a href="{% url 'profile_detail' profile.id %}">{{ profile.name }}</a></h6>
                                <small class="text-muted">{{ profile.city }} • {{ profile.get_gender_display }}</small>
                            </div>
                        {% endfor %}
                        <a href="{% url 'my_listings' %}" class="btn btn-sm btn-outline-primary">View All</a>
                    {% else %}
                        <p class="text-muted">No profiles yet.</p>
                        <a href="{% url 'create_profile' %}" class="btn btn-primary">Create Profile</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## 🎯 Template Tags and Filters

### **1. Template Tags:**

```html
<!-- Variables -->
{{ variable_name }}

<!-- Template tags -->
{% tag_name %}

<!-- Comments -->
{# This is a comment #}

<!-- If statements -->
{% if condition %}
    content
{% elif other_condition %}
    content
{% else %}
    content
{% endif %}

<!-- For loops -->
{% for item in items %}
    {{ item }}
{% empty %}
    No items found
{% endfor %}

<!-- URL generation -->
{% url 'view_name' parameter %}

<!-- CSRF token -->
{% csrf_token %}

<!-- Include other templates -->
{% include 'template_name.html' %}

<!-- Extend base template -->
{% extends 'base.html' %}
```

### **2. Template Filters:**

```html
<!-- Default value -->
{{ value|default:"No value" }}

<!-- Length -->
{{ list|length }}

<!-- Date formatting -->
{{ date|date:"F j, Y" }}

<!-- Text truncation -->
{{ text|truncatewords:30 }}

<!-- Safe HTML -->
{{ html_content|safe }}

<!-- Escape HTML -->
{{ user_input|escape }}

<!-- Upper/lower case -->
{{ text|upper }}
{{ text|lower }}

<!-- Join list -->
{{ list|join:", " }}
```

---

## 🎨 Bootstrap Integration

### **1. Grid System:**

```html
<div class="container">
    <div class="row">
        <div class="col-md-6">Left column</div>
        <div class="col-md-6">Right column</div>
    </div>
</div>
```

### **2. Components:**

```html
<!-- Cards -->
<div class="card">
    <div class="card-header">Header</div>
    <div class="card-body">Content</div>
</div>

<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-outline-secondary">Outline</button>

<!-- Alerts -->
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>

<!-- Forms -->
<form class="row g-3">
    <div class="col-md-6">
        <label class="form-label">Label</label>
        <input type="text" class="form-control">
    </div>
</form>

<!-- Badges -->
<span class="badge bg-success">Success</span>
<span class="badge bg-warning">Warning</span>
```

---

## 🔧 URL Patterns Deep Dive

### **1. Path Parameters:**

```python
# Integer parameter
path('profiles/<int:profile_id>/', views.profile_detail, name='profile_detail')

# String parameter
path('users/<str:username>/', views.user_profile, name='user_profile')

# Slug parameter
path('posts/<slug:post_slug>/', views.post_detail, name='post_detail')

# UUID parameter
path('files/<uuid:file_id>/', views.file_detail, name='file_detail')
```

### **2. Optional Parameters:**

```python
# Optional parameter
path('search/', views.search, name='search')
path('search/<str:query>/', views.search, name='search_with_query')
```

### **3. Multiple Parameters:**

```python
# Multiple parameters
path('rooms/<int:room_id>/reviews/<int:review_id>/', views.review_detail, name='review_detail')
```

---

## 🎯 Key Learning Points

### **1. URL Design:**
- **RESTful URLs:** Use nouns, not verbs
- **Hierarchical Structure:** Organize by resource type
- **Named URLs:** Use descriptive names for reverse lookup
- **Parameter Types:** Choose appropriate parameter types

### **2. Template Organization:**
- **Separation of Concerns:** Keep logic in views, presentation in templates
- **Reusability:** Use template inheritance and includes
- **Security:** Always escape user input
- **Performance:** Minimize database queries in templates

### **3. Bootstrap Integration:**
- **Responsive Design:** Use grid system for mobile-friendly layouts
- **Component Library:** Leverage Bootstrap components
- **Customization:** Override Bootstrap classes when needed
- **Consistency:** Maintain consistent styling across pages

### **4. Template Best Practices:**
- **Readability:** Use clear, descriptive variable names
- **Maintainability:** Keep templates simple and focused
- **Performance:** Avoid complex logic in templates
- **Accessibility:** Use semantic HTML and ARIA attributes

---

## 🧪 Practice Questions

1. **How would you create a URL pattern for user profiles with usernames?**
   ```python
   path('users/<str:username>/', views.user_profile, name='user_profile')
   ```

2. **How would you add pagination to a template?**
   ```html
   {% if is_paginated %}
       <nav>
           {% if page_obj.has_previous %}
               <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
           {% endif %}
           <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
           {% if page_obj.has_next %}
               <a href="?page={{ page_obj.next_page_number }}">Next</a>
           {% endif %}
       </nav>
   {% endif %}
   ```

3. **How would you create a base template with inheritance?**
   ```html
   <!-- base.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>{% block title %}{% endblock %}</title>
       <link rel="stylesheet" href="{% static 'css/style.css' %}">
   </head>
   <body>
       {% block content %}{% endblock %}
   </body>
   </html>

   <!-- child.html -->
   {% extends 'base.html' %}
   {% block title %}Page Title{% endblock %}
   {% block content %}Page content{% endblock %}
   ```

4. **How would you add conditional CSS classes?**
   ```html
   <div class="card {% if user.is_authenticated %}border-primary{% endif %}">
   ```

5. **How would you create a search form that preserves current filters?**
   ```html
   <form method="get">
       <input type="text" name="search" value="{{ request.GET.search }}">
       <input type="hidden" name="city" value="{{ request.GET.city }}">
       <button type="submit">Search</button>
   </form>
   ```

---

## 🚀 Next Steps

1. **Study URL patterns** and RESTful design principles
2. **Practice template inheritance** and includes
3. **Learn about template caching** and performance optimization
4. **Explore advanced template features** like custom template tags
5. **Understand template security** and XSS prevention

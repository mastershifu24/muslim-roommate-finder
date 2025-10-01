🗄️ Django Models Study Guide — Profile & Room System (Updated 2025)

## 1️⃣ Imports & Constants (Toolbox)

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO

# --- Define U.S. states as a dictionary (outside the class) ---
US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    # ... (50 states total)
}

# --- Major US Cities for dropdown ---
US_MAJOR_CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Charleston", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
    # ... (100+ cities total)
]
```

### **Explanation:**

- **models**: Where all field types and relationships come from (CharField, ForeignKey, etc.)
- **User**: Built-in Django authentication table
- **slugify**: Turns "John Doe" → "john-doe" (URL-friendly)
- **reverse**: Builds URLs from route names
- **post_save & receiver**: "Signals" — like events to auto-run code
- **ValidationError**: Throw an error if something is invalid
- **Image / os / BytesIO / ContentFile**: Handle images, save files
- **US_STATES & US_MAJOR_CITIES**: Predefined choices for forms and validation

**Analogy**: Think of this like your "toolbox" before building a LEGO house—you need the right tools and materials.

## 2️⃣ Profile Model (Enhanced)

### **Profile Validation Functions**
```python
def validate_profile_image_size(image):
    """Validate profile image file size (max 3MB)"""
    if image.size > 3 * 1024 * 1024:  # 3MB
        raise ValidationError("Profile image file too large ( > 3MB )")

def validate_profile_image_format(image):
    """Validate profile image format"""
    allowed_formats = ['JPEG', 'JPG', 'PNG', 'WEBP']
    try:
        with Image.open(image) as img:
            if img.format not in allowed_formats:
                raise ValidationError(f"Unsupported image format. Allowed: {', '.join(allowed_formats)}")
    except Exception as e:
        raise ValidationError("Invalid image file")
```

### **Profile Model**
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User Account")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Age")
    gender = models.CharField(max_length=20, choices=[("male", "Male"), ("female", "Female")], verbose_name="Gender")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City", db_index=True)
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="State", db_index=True)
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name="Neighborhood")
    profile_photo = models.ImageField(
        upload_to="profile_photos/", 
        verbose_name="Profile Photo",
        validators=[validate_profile_image_size, validate_profile_image_format],
        help_text="Upload your profile photo (max 3MB, JPEG/PNG/WEBP). Required for profile completion.",
        null=True, blank=True
    )
    is_looking_for_room = models.BooleanField(default=False, verbose_name="Looking for Room")
    only_eats_zabihah = models.BooleanField(default=False, verbose_name="Prefers Halal Kitchen")
    prayer_friendly = models.BooleanField(default=False, verbose_name="Prefers Prayer-Friendly Environment")
    guests_allowed = models.BooleanField(default=True, verbose_name="Allows Guests")
    bio = models.TextField(blank=True, verbose_name="Biography")
    contact_email = models.EmailField(blank=True, verbose_name="Contact Email")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Slug")
    zip_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="ZIP Code", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [
            models.Index(fields=['city', 'state']),
            models.Index(fields=['is_looking_for_room']),
            models.Index(fields=['gender']),
        ]
```

### **Key Changes from Basic Version:**

1. **Image Support**: `profile_photo` field with validation
2. **Enhanced Location**: Added `zip_code` and database indexes
3. **Timestamps**: `created_at` and `updated_at` for tracking
4. **Verbose Names**: Better admin interface labels
5. **Database Optimization**: Indexes for common queries
6. **Validation**: Custom validators for image size and format

### **Breakdown:**

- **OneToOneField(User)** → Each Profile belongs to exactly one User (1:1)
- **CASCADE** → delete Profile if User is deleted
- **PositiveIntegerField** → Only positive numbers (age)
- **ImageField** → File upload with image processing
- **db_index=True** → Database optimization for searches
- **validators** → Custom validation functions
- **verbose_name** → Human-readable field names for admin
- **Meta class** → Model configuration and database indexes

### **Edge Cases:**
- **Duplicate Profiles**: OneToOneField prevents multiple profiles per user
- **Image Size**: Validation prevents files > 3MB
- **Slug Conflicts**: Auto-generation handles duplicates with counters

### **Profile Methods**

```python
def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse("profile_detail", kwargs={"profile_id": self.id})

def is_charleston_area(self):
    if not self.city or not self.state:
        return False
    return (
        self.city.strip().lower() == "charleston"
        and self.state.strip().lower() in ["sc", "south carolina"]
    )

def is_in_area(self, cities=None, state=None, zip_codes=None):
    if not (self.city or self.state or self.zip_code):
        return False

    city_match = True
    state_match = True
    zip_match = True

    if cities:
        city_match = self.city and self.city.strip().lower() in [c.lower() for c in cities]

    if state:
        state_input = state.upper()
        state_fullnames = {v.upper(): k for k, v in US_STATES.items()}

        if state_input in US_STATES:
            state_match = self.state and self.state.strip().upper() == state_input
        elif state_input in state_fullnames:
            state_match = self.state and self.state.strip().upper() == state_fullnames[state_input]
        else:
            state_match = False

    if zip_codes:
        zip_match = self.zip_code and self.zip_code.strip() in [str(z).strip() for z in zip_codes]

    return city_match and state_match and zip_match

def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.name or self.user.username)
        slug = base_slug
        counter = 1
        while Profile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
    super().save(*args, **kwargs)
```

### **Method Explanations:**

1. **`__str__()`**: Returns profile name for admin/debugging
2. **`get_absolute_url()`**: Generates URL like `/profile/123/`
3. **`is_charleston_area()`**: Checks if profile is in Charleston, SC area
4. **`is_in_area()`**: Advanced location matching with cities, states, zip codes
5. **`save()`**: Auto-generates unique slug with conflict resolution

### **Key Improvements:**
- **Unique Slug Generation**: Handles conflicts with counter system
- **Location Intelligence**: Smart area matching for recommendations
- **Robust Validation**: Handles edge cases like missing data

## 2b️⃣ RoommateProfile Model (New)

```python
class RoommateProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="roommate_profile", verbose_name="Profile")
    budget = models.PositiveIntegerField(null=True, blank=True, verbose_name="Monthly Budget")
    occupation = models.CharField(max_length=100, blank=True, verbose_name="Occupation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", null=True, blank=True)

    class Meta:
        verbose_name = "Roommate Profile"
        verbose_name_plural = "Roommate Profiles"

    def __str__(self):
        return f"Roommate Profile: {self.profile.name}"
```

### **Purpose:**
- **Extended Profile**: Additional roommate-specific information
- **Budget Tracking**: Monthly budget for housing
- **Occupation Info**: Job/student status for compatibility

### **Relationship:**
- **OneToOne with Profile**: Each profile can have one roommate profile
- **CASCADE**: Delete roommate profile if main profile is deleted

## 3️⃣ Room System (Enhanced)

### **RoomType & Amenity Models**
```python
class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Room Type")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Amenity Name")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon Class")
    description = models.TextField(blank=True, verbose_name="Description")
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name
```

### **Room Model (Enhanced)**
```python
class Room(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="rooms", verbose_name="Owner")
    title = models.CharField(max_length=200, verbose_name="Room Title")
    description = models.TextField(verbose_name="Description", help_text="Minimum 50 characters required")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Room Type")
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name="Amenities")
    city = models.CharField(max_length=100, verbose_name="City", db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Monthly Rent")  # No cents
    available_from = models.DateField(null=True, blank=True, verbose_name="Available From")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Phone Number (Optional)")
    only_eats_zabihah = models.BooleanField(default=False, verbose_name="Halal Kitchen")
    prayer_friendly = models.BooleanField(default=False, verbose_name="Prayer-Friendly")
    guests_allowed = models.BooleanField(default=True, verbose_name="Guests Allowed")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL Slug")
    contact_email = models.EmailField(blank=True, verbose_name="Contact Email")
    is_active = models.BooleanField(default=True, verbose_name="Active Listing")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", null=True, blank=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['price']),
            models.Index(fields=['available_from']),
            models.Index(fields=['is_active']),
        ]
```

### **Key Changes from Basic Version:**

1. **Field Name Change**: `owner` → `user` (linked to Profile)
2. **Price Precision**: No decimal places (whole dollars only)
3. **Enhanced Fields**: Added `phone_number`, `is_active`, timestamps
4. **Database Optimization**: Indexes for common searches
5. **Islamic Features**: Built-in halal/prayer preferences
6. **Status Management**: `is_active` for listing management

### **Relationships:**

- **ForeignKey(user)** → one Profile can own many Rooms (1:N)
- **ForeignKey(room_type)** → one room type per Room, many Rooms can share same type
- **ManyToManyField(amenities)** → many Rooms can have many Amenities (direct relationship, no through table needed)

### **Edge Cases:**
- **Deleting a Profile** → CASCADE deletes all their rooms
- **Deleting a RoomType** → SET_NULL keeps room but removes type
- **Inactive Listings** → `is_active=False` hides from searches

### **Room Methods**
```python
def __str__(self):
    return f"{self.title} ({self.city})"

def get_absolute_url(self):
    return reverse("room_detail", kwargs={"room_id": self.id})

@property
def primary_image(self):
    """Get the primary image for this room"""
    try:
        return self.images.filter(is_primary=True).first() or self.images.first()
    except:
        return None

@property
def image_count(self):
    """Get the number of images for this room"""
    return self.images.count()

def get_price_display(self):
    """Format price for display without cents"""
    return f"${int(self.price):,}"

def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Room.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
    super().save(*args, **kwargs)
```

## 4️⃣ Messaging System (New)

### **Contact Model (Simple Messages)**
```python
class Contact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contacts", verbose_name="Profile")
    name = models.CharField(max_length=100, verbose_name="Contact Name")
    email = models.EmailField(verbose_name="Contact Email")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name} to {self.profile.name}"
```

### **Message Model (Advanced Messaging)**
```python
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="Sender")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_messages", verbose_name="Recipient")
    content = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender.name} to {self.recipient.name}"
```

### **Key Differences:**
- **Contact**: Simple contact form messages (one-way)
- **Message**: Full messaging system (two-way, read status)
- **Relationships**: Both link to Profile, not User directly

## 5️⃣ Room Images & Media (Enhanced)

### **Image Validation Functions**
```python
def validate_image_size(image):
    """Validate image file size (max 5MB)"""
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Image file too large ( > 5MB )")

def validate_image_format(image):
    """Validate image format"""
    allowed_formats = ['JPEG', 'JPG', 'PNG', 'WEBP']
    try:
        with Image.open(image) as img:
            if img.format not in allowed_formats:
                raise ValidationError(f"Unsupported image format. Allowed: {', '.join(allowed_formats)}")
    except Exception as e:
        raise ValidationError("Invalid image file")
```

### **RoomImage Model**
```python
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images", verbose_name="Room")
    image = models.ImageField(
        upload_to="room_images/", 
        verbose_name="Image",
        validators=[validate_image_size, validate_image_format],
        help_text="Upload an image (max 5MB, JPEG/PNG/WEBP)"
    )
    is_primary = models.BooleanField(default=False, verbose_name="Primary Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At", null=True, blank=True)

    class Meta:
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"Image for {self.room.title}"

    def save(self, *args, **kwargs):
        # If this is set as primary, unset all other primary images for this room
        if self.is_primary:
            RoomImage.objects.filter(room=self.room, is_primary=True).update(is_primary=False)
        
        # Auto-set as primary if it's the first image for this room
        if not self.pk and not RoomImage.objects.filter(room=self.room).exists():
            self.is_primary = True
            
        super().save(*args, **kwargs)
    
    def get_thumbnail_url(self, size=(300, 200)):
        """Generate a thumbnail URL for the image"""
        if not self.image:
            return None
        return self.image.url
    
    def get_file_size(self):
        """Get the file size in a human-readable format"""
        if not self.image:
            return "No image"
        
        try:
            size = self.image.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown size"
```

### **Key Features:**
- **Validation**: File size (5MB) and format validation
- **Primary Image Logic**: Automatic primary image management
- **Captions**: Optional image descriptions
- **Utility Methods**: Thumbnail URLs and file size display
- **Smart Ordering**: Primary images first, then by creation date

5️⃣ RoomAmenity (Bridge Table)
class RoomAmenity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)


Breakdown:

Many-to-many via a separate table

Allows extra fields later (like added_at) if needed

Edge cases:

Avoid duplicate entries for the same room/amenity combination

Deleting Room or Amenity → deletes bridge entries automatically (CASCADE)

Analogy: Like a dating app: Room “dates” Amenity. Multiple matches are allowed.

6️⃣ Room Availability
class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    available_from = models.DateField()
    available_to = models.DateField()


Breakdown:

Tracks when a Room is free

DateField → date only, no time

Edge cases:

available_to before available_from → add validation

Overlapping availability → consider constraints

Analogy: A calendar: marking when your room is open for guests.

7️⃣ Room Verification
class RoomVerification(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)


Breakdown:

One-to-one: each room has one verification record

verified → True/False

verified_at → timestamp when approved

Edge cases:

Ensure only admins can set verified=True

Slug or room deletion → verification record is removed automatically (CASCADE)

Analogy: Room = product, Verification = quality check certificate.

8️⃣ Room Favorites
class RoomFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


Breakdown:

Tracks users who “heart” a room

ForeignKey → many users can favorite many rooms (1:N)

auto_now_add=True → timestamp of when favorited

Edge cases:

Duplicate favorites → consider unique_together (user, room)

Deleting Room or User → removes favorites (CASCADE)

Analogy: Like a wish list: a user can save multiple rooms, a room can have many fans.

9️⃣ Room Reviews
class RoomReview(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


Breakdown:

rating → numeric score

comment → optional text

related_name='reviews' → access via room.reviews.all()

Edge cases:

Rating outside valid range → add validation (1-5)

Duplicate reviews → consider one review per user per room

Analogy: Yelp review: stars + comment

🔒 Validators (Image example)
def validate_image(file):
    if file.size > 5*1024*1024:
        raise ValidationError("Image too large.")
    if not file.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise ValidationError("Unsupported format.")


Explanation:

Ensures images are ≤5MB

Only JPG/PNG/WEBP allowed

Edge cases:

Large file uploads → breaks storage or slow load

Unsupported extensions → prevent crash or security issues

Analogy: Security guard at the door checking allowed items

🔔 Signals (auto-create Profile)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


Explanation:

Auto-create Profile whenever a new User is created

Keep Profile updated whenever User changes

Analogy: Butler: automatically sets up things for new people

Edge cases:

Circular save → careful with overriding save method

Existing Profiles → check before creating new one

🔑 Relationship Mnemonics
Django Field	Relationship	Analogy
OneToOneField	1 ↔ 1	Passport attached to Person
ForeignKey	Many → 1	Children belong to Parent
ManyToManyField	Many ↔ Many	Friends; Rooms ↔ Amenities
Signal	Event listener	Butler automatically doing tasks
Validator	Field checker	Security guard at door
✅ Key Edge Cases Summary

OneToOne → duplicate relationships, deletion of parent

ForeignKey → optional vs required, deletion behavior (CASCADE, SET_NULL)

ManyToMany → duplicates, custom bridge table logic

DateFields → available_to < available_from

BooleanFields → default values, required vs optional

SlugField → duplicates, special characters
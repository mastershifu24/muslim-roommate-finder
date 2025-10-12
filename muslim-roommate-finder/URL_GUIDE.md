# 🌐 URL Guide - Muslim Roommate Finder

## 📋 **All Available URLs:**

### **Main Pages:**
- 🏠 **Home:** http://127.0.0.1:8000/
- 👥 **Browse Profiles:** http://127.0.0.1:8000/profiles/
- 🔍 **Advanced Search:** http://127.0.0.1:8000/advanced-search/

### **Authentication:**
- 📝 **Register:** http://127.0.0.1:8000/register/
- 🔐 **Login:** http://127.0.0.1:8000/login/
- 🚪 **Logout:** http://127.0.0.1:8000/logout/

### **User Dashboard:**
- 📊 **Dashboard:** http://127.0.0.1:8000/dashboard/
- 📋 **My Listings:** http://127.0.0.1:8000/my-listings/
- 📧 **Inbox:** http://127.0.0.1:8000/inbox/

### **Profile Management:**
- ➕ **Create Profile:** http://127.0.0.1:8000/create/
- 👤 **View Profile:** http://127.0.0.1:8000/profile/{id}/
- ✏️ **Edit Profile:** http://127.0.0.1:8000/profile/{id}/edit/
- 🗑️ **Delete Profile:** http://127.0.0.1:8000/profile/{id}/delete/
- 📨 **Contact Profile:** http://127.0.0.1:8000/profile/{id}/contact/

### **Room Management:**
- ➕ **Create Room:** http://127.0.0.1:8000/rooms/create/
- 🏠 **View Room:** http://127.0.0.1:8000/rooms/{id}/
- ✏️ **Edit Room:** http://127.0.0.1:8000/rooms/{id}/edit/
- 🗑️ **Delete Room:** http://127.0.0.1:8000/rooms/{id}/delete/

### **Messaging:**
- ✉️ **Compose Message:** http://127.0.0.1:8000/compose/
- ✉️ **Compose to Profile:** http://127.0.0.1:8000/compose/{profile_id}/

### **Admin:**
- 🔧 **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🎯 **To See Profile Photos:**

### **Option 1: Browse Profiles Page**
Visit: **http://127.0.0.1:8000/profiles/**

You'll see:
- Grid of profile cards
- Profile photos (or fallback icons)
- Names, ages, locations
- Islamic preferences badges

### **Option 2: Home Page**
Visit: **http://127.0.0.1:8000/**

Scroll down to "People Looking for Rooms" section

### **Option 3: Individual Profile**
Click any profile or visit directly:
- http://127.0.0.1:8000/profile/1/
- http://127.0.0.1:8000/profile/2/
- http://127.0.0.1:8000/profile/3/
- etc.

---

## 👥 **Sample Users with Photos:**

Login with these to test:
1. **abdullah_malik / password123** - Has photo
2. **sarah_khan / password123** - Has photo
3. **omar_ibrahim / password123** - Has photo
4. **layla_ahmed / password123** - Has photo
5. **mohammed_ali / password123** - Has photo

---

## 📸 **If Photos Still Don't Show:**

### **Quick Fix #1: Check Server is Running**
```bash
# Stop any existing server (Ctrl+C)
python manage.py runserver
```

### **Quick Fix #2: Run Photo Link Command**
```bash
python manage.py link_profile_photos
```

### **Quick Fix #3: Download Fresh Photos**
```bash
python manage.py download_sample_photos
```

### **Quick Fix #4: Check Media Files**
Visit: http://127.0.0.1:8000/media/profile_photos/abdullah_malik_profile.jpg

If this shows the image, then photos exist and templates just need refreshing.

---

## 🔍 **Debug Steps:**

1. **Check Profile Count:**
   ```bash
   python manage.py shell -c "from core.models import Profile; print(Profile.objects.count())"
   ```

2. **Check Photos Exist:**
   ```bash
   python manage.py shell -c "from core.models import Profile; print([p.profile_photo.name for p in Profile.objects.all() if p.profile_photo])"
   ```

3. **View in Browser:**
   - Open http://127.0.0.1:8000/profiles/
   - Right-click → Inspect → Console
   - Look for any image loading errors

---

## ✨ **What Should Work:**

When you visit **http://127.0.0.1:8000/profiles/** you should see:

```
┌─────────────────────────┐
│  [Photo]  or  [A]       │ ← Profile photo or initial
│  Abdullah Malik, 26     │
│  Seattle | Male         │
│  📍 Tech professional   │
│  ✓ Zabihah ✓ Prayer    │
└─────────────────────────┘
```

Repeated for all 5 profiles in a responsive grid.

---

## 🎯 **Current Status:**

- ✅ Server should be running at http://127.0.0.1:8000/
- ✅ 5 profiles exist in database
- ✅ 5 profile photos downloaded
- ✅ Templates configured to show photos
- ✅ All tests passing

**Try the URL again:** http://127.0.0.1:8000/profiles/


# 🚀 How to Start the Server Properly

## 📋 **Steps:**

### **1. Stop Any Running Servers:**
Press `Ctrl + C` in any terminal windows running Django

### **2. Start Fresh:**
```bash
cd muslim-roommate-finder
python manage.py runserver
```

### **3. You Should See:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 12, 2025 - XX:XX:XX
Django version X.X, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### **4. Test These URLs:**

1. **Direct Image Test:**
   http://127.0.0.1:8000/media/profile_photos/abdullah_malik_profile.jpg
   ✅ Should show an image

2. **Browse Profiles:**
   http://127.0.0.1:8000/profiles/
   ✅ Should show 5 profiles with photos

3. **Home Page:**
   http://127.0.0.1:8000/
   ✅ Should work normally

---

## 🔍 **If Images Still Don't Show:**

### **Check 1: View HTML Source**
- Right-click → View Page Source
- Search for: `profile_photo.url`
- You should see: `src="/media/profile_photos/..."`

### **Check 2: Browser Console**
- Press F12
- Check Console tab for errors
- Look for 404 errors on image URLs

### **Check 3: Network Tab**
- Press F12 → Network tab
- Reload page
- Filter by "Img"
- See if images are loading (200 status) or failing (404 status)

---

## ✅ **Current Status:**

Based on diagnostics:
- ✅ 5 profiles exist
- ✅ All have photos in database
- ✅ All photo files exist on disk
- ✅ MEDIA_URL configured: /media/
- ✅ MEDIA_ROOT configured correctly
- ✅ DEBUG = True
- ✅ URL patterns include media serving
- ✅ Templates use correct syntax

**Everything is configured correctly!**

The issue is likely:
1. Browser cache (try Ctrl+Shift+R)
2. Server not restarted
3. Viewing wrong page

---

## 🎯 **Quick Test:**

**Open this EXACT URL in your browser:**
```
http://127.0.0.1:8000/media/profile_photos/abdullah_malik_profile.jpg
```

If you see a person's face photo → Everything works, just refresh browser!


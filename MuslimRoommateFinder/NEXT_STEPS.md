# 🚀 Next Steps - Start Testing Your Mobile App!

## Right Now (5 minutes):

### 1. Update the API URL
Open `src/api/client.js` and change line 8:

**Find your computer's IP address:**
```powershell
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (probably starts with 192.168 or 10.0)

**Then update:**
```javascript
const API_BASE_URL = 'http://YOUR_IP_HERE:8000/api';
// Example: 'http://10.0.0.209:8000/api'
```

### 2. Start Django Backend
```powershell
cd C:\Users\hurri\OneDrive\Desktop\muslim-roommate-finder\muslim-roommate-finder
python manage.py runserver 0.0.0.0:8000
```

Keep this terminal running!

### 3. Start React Native App
**Open a NEW terminal:**
```powershell
cd C:\Users\hurri\OneDrive\Desktop\muslim-roommate-finder\MuslimRoommateFinder
npm start
```

### 4. Test on Your Phone
1. Install **Expo Go** from App Store (free)
2. Connect phone to **same WiFi** as computer
3. Open Expo Go app
4. Scan the QR code from your terminal

**BOOM! Your app is running!** 📱

---

## What to Test:

✅ Register a new account
✅ Fill out your profile
✅ Add your WhatsApp number
✅ See compatibility matches on Home screen
✅ Browse profiles
✅ Tap a profile to see details
✅ Click WhatsApp button (should open WhatsApp)
✅ Edit your profile
✅ Log out and log back in
✅ Search for profiles

---

## Troubleshooting:

### "Cannot connect to API"
- Django must be running on `0.0.0.0:8000`
- Check your IP address is correct in `src/api/client.js`
- Phone and computer must be on same WiFi

### "App crashes"
- Check terminal for error messages
- Try: `npm start -- --clear` (clears cache)

### "Can't scan QR code"
- Make sure Expo Go app is installed
- Try typing the URL manually in Expo Go

---

## When You're Ready to Deploy:

### Option 1: Keep Local Testing
- Works great for demos
- Show to friends on your WiFi
- Good for getting initial feedback

### Option 2: Deploy Backend to Render
- Makes app work anywhere (not just local WiFi)
- Change API_BASE_URL to: `https://your-app.onrender.com/api`
- Now anyone can test the app!

### Option 3: Build for App Stores
```bash
npm install -g eas-cli
eas login
eas build --platform android  # Start with Android (easier)
```

---

## 🎯 Your Mission (if you choose to accept it):

1. **Today:** Get the app running on your phone
2. **This Week:** Show 5 people and get feedback
3. **Next Week:** Post in MSA/mosque groups
4. **This Month:** Get 50 users and iterate

---

## 💬 Demo Script (What to Say):

> "Hey, I built a mobile app to help Muslims find roommates. It's way better than Facebook groups because it automatically calculates compatibility based on things like zabihah, prayer times, and location. Want to try it?"

> "Just download 'Expo Go' from the App Store, and I'll show you how it works."

---

**You're ready to go! Just follow steps 1-4 above.** 🚀


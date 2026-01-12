# Muslim Roommate Finder - Mobile App Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js v20+ (you have v20.10.0 ✅)
- npm v10+ (you have v10.2.3 ✅)
- Expo Go app on your phone (download from App Store or Google Play)
- Your Django backend running

### Step 1: Update Django API URL

Open `src/api/client.js` and update the API URL:

```javascript
// For local testing (same WiFi):
const API_BASE_URL = 'http://YOUR_COMPUTER_IP:8000/api';

// For production (after deploying to Render):
const API_BASE_URL = 'https://your-render-url.onrender.com/api';
```

**Find your computer's IP address:**
- Windows: Open PowerShell and run `ipconfig` - look for "IPv4 Address"
- Mac/Linux: Run `ifconfig` or `ip addr`

### Step 2: Start Django Backend

```powershell
# In your Django project folder
cd muslim-roommate-finder
python manage.py runserver 0.0.0.0:8000
```

Keep this running!

### Step 3: Start React Native App

```powershell
# In the MuslimRoommateFinder folder
cd MuslimRoommateFinder
npm start
```

### Step 4: Test on Your Phone

1. Install **Expo Go** from App Store (iOS) or Google Play (Android)
2. Make sure your phone is on the **same WiFi** as your computer
3. Open Expo Go app
4. Scan the QR code shown in your terminal

The app will load on your phone!

## 📱 Features

### Screens Built:
- ✅ **Login** - Sign in with username/password
- ✅ **Register** - Create new account
- ✅ **Home** - Dashboard with top matches and compatibility scores
- ✅ **Browse** - View all profiles with search
- ✅ **Profile Detail** - See detailed profile with WhatsApp contact
- ✅ **My Profile** - Edit your profile and preferences
- ✅ **Messages** - View inbox (basic implementation)

### Key Features:
- 🔐 Full authentication (login/register/logout)
- 🤝 Smart compatibility matching (same algorithm as web)
- 💬 WhatsApp integration (click to chat)
- 📧 Email contact buttons
- 🔍 Search and browse profiles
- ⚙️ Full profile editing
- 📱 Bottom tab navigation
- 🔄 Pull to refresh

## 🎨 What Works

1. **Authentication Flow**
   - Register new users
   - Login existing users
   - Auto-login on app restart (token stored)
   - Logout with confirmation

2. **Profile Management**
   - View your profile
   - Edit all fields (name, age, gender, location, bio)
   - Update preferences (zabihah, prayer, guests)
   - Add WhatsApp number for easy contact

3. **Browse & Match**
   - See all profiles
   - Search by name/location
   - View compatibility scores
   - Tap to see full profile

4. **Contact**
   - WhatsApp click-to-chat buttons
   - Email links
   - Direct profile viewing

## 🚧 Next Steps (If You Want)

### Additional Features to Add:
1. **Image Upload** - Add camera/gallery support
2. **Room Listings** - Show available rooms in the app
3. **Push Notifications** - For new messages
4. **Real-time Messaging** - Chat within the app
5. **Filters** - Advanced search filters

### Building for App Stores:

#### iOS (requires Mac):
```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build for iOS
eas build --platform ios
```

#### Android:
```bash
# Build APK for testing
eas build --platform android --profile preview

# Build for Google Play Store
eas build --platform android --profile production
```

## 🐛 Troubleshooting

### "Cannot connect to API"
- Make sure Django is running on `0.0.0.0:8000`
- Check your computer's IP address is correct in `src/api/client.js`
- Make sure phone and computer are on same WiFi
- Check Django's `ALLOWED_HOSTS` includes your IP

### "App won't load"
- Clear Expo cache: `npm start -- --clear`
- Restart both Django and Expo servers
- Check terminal for errors

### "Module not found"
- Run `npm install` again
- Clear cache: `npm start -- --clear`

## 📝 Important Notes

### API Integration
The app connects to your Django backend using the REST API we created:
- `/api/auth/login/` - Login
- `/api/auth/register/` - Register
- `/api/profiles/` - List profiles
- `/api/profiles/me/` - Get/update current user profile
- `/api/messages/` - Messaging

### Data Storage
- Auth token stored in AsyncStorage (persists across app restarts)
- User stays logged in until they click logout

### Development vs Production
- **Development**: Use your local IP address (e.g., `http://10.0.0.209:8000/api`)
- **Production**: Use your Render URL (e.g., `https://muslim-roommate-finder.onrender.com/api`)

## 🎯 What This Gives You

✅ **Real mobile app** that works on iOS and Android
✅ **Native look and feel** with smooth navigation
✅ **Same features** as your web app
✅ **Can be submitted to App Stores** (with some additional setup)
✅ **Professional matching algorithm** built-in
✅ **Easy to show** to mosques, MSAs, and potential users

## 🔥 Demo It Now!

1. Start the servers (Django + Expo)
2. Open on your phone
3. Register a new account
4. Fill out your profile
5. See matches with compatibility scores!
6. Click WhatsApp to contact someone

This is **WAY better** than just a Facebook group!

---

**Need help?** Check the terminal output for errors, and make sure all servers are running.


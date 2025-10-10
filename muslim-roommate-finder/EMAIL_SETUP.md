# 📧 Email Setup for Feedback Notifications

This guide will help you set up email notifications so you receive feedback directly in your inbox.

## 🚀 Quick Setup

### **Option 1: Gmail (Recommended)**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Set Environment Variables**:
   ```bash
   export EMAIL_HOST_USER="your-email@gmail.com"
   export EMAIL_HOST_PASSWORD="your-16-character-app-password"
   export ADMIN_EMAIL="your-email@gmail.com"
   ```

### **Option 2: Other Email Providers**

Update the settings in `config/settings.py`:

```python
EMAIL_HOST = 'smtp.outlook.com'  # For Outlook
EMAIL_HOST = 'smtp.yahoo.com'    # For Yahoo
EMAIL_HOST = 'your-provider-smtp.com'  # For others
```

## 🔧 Configuration

### **For Development (Console Output)**
Emails will be printed to the console - no setup needed!

### **For Production (Real Emails)**
Set these environment variables:

```bash
# Required
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com

# Optional
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## 📱 What You'll Receive

When someone submits feedback, you'll get an email with:

- **Subject**: 🕌 New Feedback: [Type] - [Title]
- **Content**: All feedback details, user info, technical details
- **Direct Link**: To admin panel for responding
- **Beautiful HTML Format**: Easy to read and respond

## 🧪 Testing

1. **Submit test feedback** using the form
2. **Check your email** (or console in development)
3. **Click admin link** to respond

## 🔒 Security Notes

- **Never commit** your email credentials to Git
- **Use app passwords** instead of your main password
- **Environment variables** keep credentials secure
- **Console backend** is safe for development

## 📋 Email Template Features

✅ **Priority color coding** (Low/Medium/High/Urgent)  
✅ **Feedback type badges** (Bug/Feature/UI/General/Praise)  
✅ **Direct admin links** for quick responses  
✅ **Technical info** (browser, user, timestamp)  
✅ **Mobile-friendly** HTML design  
✅ **Islamic theme** colors and styling  

## 🆘 Troubleshooting

**Email not sending?**
- Check your app password is correct
- Verify 2FA is enabled on your account
- Check console for error messages

**Gmail blocking?**
- Check "Less secure app access" (if using password)
- Use app password instead of regular password
- Check spam folder

**Want to change email provider?**
- Update `EMAIL_HOST` in settings
- Check provider's SMTP settings
- Update port if needed (587 for TLS, 465 for SSL)

---

## 🎯 Next Steps

1. **Set up your email credentials**
2. **Test with sample feedback**
3. **Share the app** with testers
4. **Receive feedback notifications** in real-time!

**Your feedback system is now fully connected to your email! 📧✨**

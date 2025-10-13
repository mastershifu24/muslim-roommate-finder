# 🎨 Muslim-Friendly Avatar Guide

## Current Solution
The app currently uses DiceBear's "Lorelei" style avatars which provide diverse, professional illustrations.

## Better Options for Muslim Representation

### Option 1: Curated Stock Photos (RECOMMENDED)
Download free, respectful photos of Muslims from these sources:

1. **Pexels** (Free, no attribution required)
   - Search: "muslim woman hijab portrait"
   - Search: "muslim man kufi portrait"
   - Download 400x400 JPGs
   - Save to: `media/profile_photos/`

2. **Unsplash** (Free, high quality)
   - Search: "modest fashion hijab"
   - Search: "muslim prayer kufi"
   - Download and save to project

### Option 2: Islamic Avatar Illustrations

**Free Resources:**
- **Fatar App**: Create custom Islamic avatars (faceless, modest)
- **IconScout Islamic Pack**: Professional Muslim avatars
- **Vector EPS Muslim Avatars**: Diverse Muslim representations

### Option 3: Commission Custom Art
For the most authentic representation:
- Hire a Muslim artist on Fiverr ($20-50)
- Get 10-15 diverse, modest avatars
- Includes hijabs, kufis, niqabs, various skin tones

## How to Add Custom Photos

1. **Download photos** (400x400 px recommended)
2. **Save to** `media/profile_photos/`
3. **Run command:**
   ```bash
   python manage.py link_profile_photos
   ```

## Current Avatar Style
- **API**: DiceBear Lorelei
- **Style**: Realistic illustrated portraits
- **Backgrounds**: Neutral gray tones
- **Diversity**: Varied features based on username seed

## To Switch to Real Photos:
1. Get 5-10 diverse Muslim photos
2. Name them: `{username}_profile.jpg`
3. Place in `media/profile_photos/`
4. Photos will automatically show instead of generated avatars

## Recommended Photo Specs:
- **Format**: JPG or PNG
- **Size**: 400x400 pixels (square)
- **Style**: Professional headshot
- **Background**: Neutral or blurred
- **Content**: Modest, respectful attire


"""Generate PWA icons for Muslim Roommate Finder"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple app icon with mosque emoji or text"""
    # Create green background
    img = Image.new('RGB', (size, size), color='#28a745')
    draw = ImageDraw.Draw(img)
    
    # Add white circle in center
    padding = size // 6
    draw.ellipse([padding, padding, size-padding, size-padding], fill='white')
    
    # Add text/emoji
    try:
        # Try to load a nice font
        font_size = size // 3
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                font = ImageFont.load_default()
        
        # Draw "MRF" text
        text = "MRF"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2 - size // 20)
        draw.text(position, text, fill='#28a745', font=font)
        
    except Exception as e:
        print(f"Font error: {e}")
        # Fallback: just a green circle with white background
        pass
    
    # Save
    img.save(output_path, 'PNG')
    print(f"Created {output_path}")

# Create output directory
os.makedirs('static/images', exist_ok=True)

# Generate icons
create_icon(192, 'static/images/icon-192.png')
create_icon(512, 'static/images/icon-512.png')

print("\n✅ PWA icons generated successfully!")
print("Icons saved to static/images/")


#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')
django.setup()

from apps.gallery.models import Artwork

print("🔍 DEBUGGING CLOUDINARY URLS")
print("=" * 50)

# Get the latest artwork
try:
    latest_artwork = Artwork.objects.order_by('-created_at').first()
    
    if latest_artwork:
        print(f"📸 Latest Artwork: {latest_artwork.title}")
        print(f"👤 Artist: {latest_artwork.artist.username}")
        print(f"📅 Created: {latest_artwork.created_at}")
        print()
        
        # Check image field
        print("🖼️  IMAGE FIELD:")
        print(f"   Field name: {latest_artwork.image.name}")
        print(f"   Field URL: {latest_artwork.image.url}")
        print(f"   Field exists: {bool(latest_artwork.image)}")
        print()
        
        # Check thumbnail field
        print("🔳 THUMBNAIL FIELD:")
        print(f"   Field name: {latest_artwork.thumbnail.name if latest_artwork.thumbnail else 'None'}")
        print(f"   Field URL: {latest_artwork.thumbnail.url if latest_artwork.thumbnail else 'None'}")
        print(f"   Field exists: {bool(latest_artwork.thumbnail)}")
        print()
        
        # Test our custom template filters
        from apps.gallery.templatetags.cloudinary_tags import cloudinary_thumbnail, cloudinary_url
        
        print("🏷️  TEMPLATE FILTER RESULTS:")
        if latest_artwork.image:
            thumb_url = cloudinary_thumbnail(latest_artwork.image, "300x300")
            print(f"   Thumbnail 300x300: {thumb_url}")
            
            optimized_url = cloudinary_url(latest_artwork.image, "q_auto,f_auto")
            print(f"   Optimized URL: {optimized_url}")
        
    else:
        print("❌ No artworks found in database")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("📋 Copy one of the URLs above and test it in your browser!")
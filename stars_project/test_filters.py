#!/usr/bin/env python
import os
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')
os.environ['USE_CLOUDINARY_IN_DEV'] = 'True'

import django
django.setup()

# Test our template filters directly
from apps.gallery.templatetags.cloudinary_tags import cloudinary_thumbnail, cloudinary_url

print("🔍 TESTING TEMPLATE FILTERS DIRECTLY")
print("=" * 60)

# Create a mock image field with the problematic URL
class MockImageField:
    def __init__(self, name):
        self.name = name
        self.url = f"/media/{name}"

# Test with the actual problematic URL from your database
test_image = MockImageField("https:/res.cloudinary.com/dl3d6vid3/artworks/1_qgy5h5")

print(f"📥 Input: {test_image.name}")
print()

# Test thumbnail filter
thumbnail_url = cloudinary_thumbnail(test_image, "300x300")
print(f"🔳 Thumbnail 300x300:")
print(f"   {thumbnail_url}")
print()

# Test cloudinary_url filter
optimized_url = cloudinary_url(test_image, "q_auto,f_auto")
print(f"🖼️  Optimized URL:")
print(f"   {optimized_url}")
print()

# Test with basic transformations
basic_url = cloudinary_url(test_image, "")
print(f"🔧 Basic URL:")
print(f"   {basic_url}")

print("\n" + "=" * 60)
print("📋 Test these URLs in your browser!")
print("🎯 Expected format: https://res.cloudinary.com/dl3d6vid3/image/upload/...")
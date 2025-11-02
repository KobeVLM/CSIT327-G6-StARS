#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')
django.setup()

from django.conf import settings

print("🔍 CLOUDINARY CONFIGURATION CHECK")
print("=" * 50)

print(f"DEBUG: {settings.DEBUG}")
print(f"USE_CLOUDINARY_IN_DEV: {os.getenv('USE_CLOUDINARY_IN_DEV', 'Not set')}")
print()

print("Environment Variables:")
print(f"  CLOUDINARY_URL: {os.getenv('CLOUDINARY_URL', 'Not set')}")
print(f"  CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME', 'Not set')}")
print(f"  CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY', 'Not set')}")
print(f"  CLOUDINARY_API_SECRET: {'***' if os.getenv('CLOUDINARY_API_SECRET') else 'Not set'}")
print()

print("Django Settings:")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  DEFAULT_FILE_STORAGE: {settings.STORAGES.get('default', {}).get('BACKEND', 'Not set')}")
print()

# Test Cloudinary import
try:
    import cloudinary
    print(f"Cloudinary config: {cloudinary.config()}")
except Exception as e:
    print(f"Cloudinary import error: {e}")

print("=" * 50)
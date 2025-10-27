#!/usr/bin/env python
"""
Test script to upload an image directly to Cloudinary through Django models
"""
import os
import sys
from pathlib import Path

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')

try:
    import django
    django.setup()
    
    from django.contrib.auth.models import User
    from apps.gallery.models import Artwork, Category
    from django.core.files.uploadedfile import SimpleUploadedFile
    import cloudinary.uploader
    
    print("=== Cloudinary Upload Test ===")
    
    # Test direct Cloudinary upload
    print("1. Testing direct Cloudinary upload...")
    
    # You can replace this with path to any test image
    test_image_path = input("Enter path to test image (or press Enter to skip): ").strip()
    
    if test_image_path and Path(test_image_path).exists():
        try:
            result = cloudinary.uploader.upload(test_image_path)
            print(f"✅ Direct upload successful!")
            print(f"   URL: {result['url']}")
            print(f"   Public ID: {result['public_id']}")
        except Exception as e:
            print(f"❌ Direct upload failed: {e}")
    else:
        print("Skipping direct upload test")
    
    # Test Django model upload (if you want to create an artwork)
    create_artwork = input("Create test artwork? (y/n): ").lower() == 'y'
    
    if create_artwork:
        try:
            # Get or create a user
            user, created = User.objects.get_or_create(
                username='test_user',
                defaults={'email': 'test@example.com'}
            )
            
            # Get or create a category
            category, created = Category.objects.get_or_create(
                name='Test Category',
                defaults={'slug': 'test-category', 'description': 'Test category'}
            )
            
            print(f"✅ Test setup complete")
            print(f"   User: {user.username}")
            print(f"   Category: {category.name}")
            print("Now you can upload artwork through the web interface!")
            
        except Exception as e:
            print(f"❌ Test setup failed: {e}")
    
except Exception as e:
    print(f"❌ Script failed: {e}")
    import traceback
    traceback.print_exc()
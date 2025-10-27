#!/usr/bin/env python
import os
import sys

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')

try:
    import django
    django.setup()
    
    # Test environment variables
    print("=== Environment Variables ===")
    print(f"CLOUDINARY_URL: {os.getenv('CLOUDINARY_URL')}")
    print(f"CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
    print(f"CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
    
    # Test Cloudinary import and configuration
    import cloudinary
    
    # Cloudinary should be configured by Django settings
    
    print("\n=== Cloudinary Configuration ===")
    config = cloudinary.config()
    print(f"Cloud Name: {config.cloud_name}")
    print(f"API Key: {config.api_key}")
    print(f"Secure: {config.secure}")
    
    # Test upload capability
    print("\n=== Testing Cloudinary Connection ===")
    try:
        result = cloudinary.api.ping()
        print("✅ Cloudinary connection successful!")
        print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Cloudinary connection failed: {e}")
        
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
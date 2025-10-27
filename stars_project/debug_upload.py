#!/usr/bin/env python
"""
Debug script to test Cloudinary configuration and upload functionality
"""
import os
import sys

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')

try:
    import django
    django.setup()
    
    from django.conf import settings
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    import cloudinary
    import cloudinary.uploader
    
    print("=== Cloudinary Configuration Debug ===")
    
    # Check environment variables
    print("\n1. Environment Variables:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
    print(f"   CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
    print(f"   CLOUDINARY_API_SECRET: {'***' if os.getenv('CLOUDINARY_API_SECRET') else 'None'}")
    print(f"   USE_CLOUDINARY_IN_DEV: {os.getenv('USE_CLOUDINARY_IN_DEV')}")
    
    # Check Django settings
    print("\n2. Django Settings:")
    print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    if hasattr(settings, 'STORAGES'):
        print(f"   STORAGES (default): {settings.STORAGES.get('default', 'Not set')}")
    
    # Check Cloudinary config
    print("\n3. Cloudinary Configuration:")
    config = cloudinary.config()
    print(f"   Cloud Name: {config.cloud_name}")
    print(f"   API Key: {config.api_key}")
    print(f"   Secure: {config.secure}")
    
    # Test storage backend
    print("\n4. Testing Storage Backend:")
    print(f"   Storage class: {type(default_storage).__name__}")
    print(f"   Storage module: {type(default_storage).__module__}")
    
    # Test file upload
    print("\n5. Testing File Upload:")
    try:
        test_content = ContentFile(b"Hello World Test", name="test.txt")
        file_path = default_storage.save("test/test_upload.txt", test_content)
        file_url = default_storage.url(file_path)
        
        print(f"   ✅ Upload successful!")
        print(f"   File path: {file_path}")
        print(f"   File URL: {file_url}")
        
        # Clean up
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            print(f"   ✅ Cleanup successful!")
            
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test direct Cloudinary
    print("\n6. Testing Direct Cloudinary Upload:")
    try:
        result = cloudinary.uploader.upload_resource(
            ContentFile(b"Direct test content"), 
            resource_type="raw",
            public_id="test_direct_upload"
        )
        print(f"   ✅ Direct upload successful!")
        print(f"   URL: {result.get('url')}")
        
        # Clean up
        cloudinary.uploader.destroy("test_direct_upload", resource_type="raw")
        print(f"   ✅ Direct cleanup successful!")
        
    except Exception as e:
        print(f"   ❌ Direct upload failed: {e}")
        
except Exception as e:
    print(f"❌ Script failed: {e}")
    import traceback
    traceback.print_exc()
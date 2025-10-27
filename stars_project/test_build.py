#!/usr/bin/env python3
"""
Test script to simulate Render build environment
"""
import os
import sys
import subprocess

# Set environment variables like Render would
os.environ['DJANGO_SETTINGS_MODULE'] = 'stars.settings'
os.environ['BUILD_PHASE'] = 'true'
os.environ['DEBUG'] = 'False'

# Set a dummy secret key for testing
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'test-secret-key-for-build-only'

# Clear any existing Django setup
if 'django' in sys.modules:
    del sys.modules['django']

print("Testing Django setup with build environment...")

try:
    # Test Django import
    import django
    print(f"✓ Django version: {django.get_version()}")
    
    # Test settings import
    from django.conf import settings
    print(f"✓ Settings imported successfully")
    print(f"✓ DEBUG: {settings.DEBUG}")
    print(f"✓ INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
    
    # Test Django setup
    django.setup()
    print("✓ Django setup completed")
    
    # Test management commands
    from django.core.management import call_command
    
    print("\nTesting management commands...")
    
    # Test check command
    print("Running Django check...")
    call_command('check')
    print("✓ Django check passed")
    
    # Test collectstatic in dry-run mode
    print("Testing collectstatic (dry-run)...")
    call_command('collectstatic', '--dry-run', verbosity=0)
    print("✓ Collectstatic test passed")
    
    print("\n🎉 All tests passed! Build should work on Render.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
#!/usr/bin/env python
import os
import sys
import traceback

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')

try:
    import django
    django.setup()
    
    from django.db import connection
    print("Testing Supabase connection...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Connection successful! Result: {result}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    traceback.print_exc()

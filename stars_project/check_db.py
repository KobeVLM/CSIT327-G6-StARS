#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')
django.setup()

from django.db import connection

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print("Tables in Supabase database:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Check specific Django auth tables
        cursor.execute("SELECT COUNT(*) FROM auth_user;")
        user_count = cursor.fetchone()[0]
        print(f"\nUsers in auth_user table: {user_count}")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM users_userprofile;")
            profile_count = cursor.fetchone()[0]
            print(f"Profiles in users_userprofile table: {profile_count}")
        except Exception as e:
            print(f"Error checking profiles: {e}")

if __name__ == '__main__':
    list_tables()

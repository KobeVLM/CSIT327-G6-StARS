#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stars.settings')
django.setup()

from django.contrib.auth.models import User
from gallery.models import Artwork
from moderation.models import Report, UserViolation

def create_test_data():
    print("Creating test data for moderation system...")
    
    # Create some test users
    user1, created = User.objects.get_or_create(
        username='testuser1',
        defaults={
            'email': 'test1@example.com',
            'first_name': 'Test',
            'last_name': 'User1'
        }
    )
    
    user2, created = User.objects.get_or_create(
        username='testuser2',
        defaults={
            'email': 'test2@example.com',
            'first_name': 'Test',
            'last_name': 'User2'
        }
    )
    
    user3, created = User.objects.get_or_create(
        username='reporter',
        defaults={
            'email': 'reporter@example.com',
            'first_name': 'Reporter',
            'last_name': 'User'
        }
    )
    
    # Create some test artworks
    artwork1, created = Artwork.objects.get_or_create(
        title='Inappropriate Content',
        defaults={
            'artist': user1,
            'description': 'This artwork contains inappropriate content that should be moderated.',
            'image': 'uploads/test1.jpg'
        }
    )
    
    artwork2, created = Artwork.objects.get_or_create(
        title='Spam Artwork',
        defaults={
            'artist': user2,
            'description': 'This is spam artwork used for testing moderation.',
            'image': 'uploads/test2.jpg'
        }
    )
    
    # Create some reports
    report1, created = Report.objects.get_or_create(
        reported_by=user3,
        artwork=artwork1,
        defaults={
            'reason': 'inappropriate',
            'description': 'This artwork contains inappropriate content that violates community guidelines.',
            'status': 'pending'
        }
    )
    
    report2, created = Report.objects.get_or_create(
        reported_by=user3,
        artwork=artwork2,
        defaults={
            'reason': 'spam',
            'description': 'This appears to be spam content.',
            'status': 'pending'
        }
    )
    
    # Get or create staff user for actioned_by field
    staff_user = User.objects.get(username='staff')
    
    # Create some user violations
    violation1, created = UserViolation.objects.get_or_create(
        user=user1,
        defaults={
            'violation_type': 'inappropriate',
            'description': 'Posted inappropriate content',
            'action_taken': 'warning',
            'actioned_by': staff_user
        }
    )
    
    violation2, created = UserViolation.objects.get_or_create(
        user=user2,
        defaults={
            'violation_type': 'spam',
            'description': 'Posted spam content',
            'action_taken': 'warning',
            'actioned_by': staff_user
        }
    )
    
    print("Test data created successfully!")
    print(f"- Created {User.objects.count()} users")
    print(f"- Created {Artwork.objects.count()} artworks") 
    print(f"- Created {Report.objects.count()} reports")
    print(f"- Created {UserViolation.objects.count()} violations")

if __name__ == '__main__':
    create_test_data()
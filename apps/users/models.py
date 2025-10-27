from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Profile Information
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    # Social Media Links
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    behance_url = models.URLField(blank=True)
    dribbble_url = models.URLField(blank=True)
    
    # Gamification (keeping existing field names for compatibility)
    level = models.PositiveIntegerField(default=1)
    total_xp = models.PositiveIntegerField(default=0)  # Renamed from xp for compatibility
    artwork_created = models.PositiveIntegerField(default=0)
    total_likes_received = models.PositiveIntegerField(default=0)
    total_shares_received = models.PositiveIntegerField(default=0)
    
    # Preferences
    is_profile_public = models.BooleanField(default=True)
    show_email_publicly = models.BooleanField(default=False)
    allow_messages = models.BooleanField(default=True)
    
    # Notification Preferences (keeping existing field names)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    notify_on_like = models.BooleanField(default=True)
    notify_on_share = models.BooleanField(default=True)
    notify_on_follow = models.BooleanField(default=True)
    notify_on_badge = models.BooleanField(default=True)
    notify_on_contest = models.BooleanField(default=True)
    
    # Theme Preferences (keeping existing field names)
    dark_mode = models.BooleanField(default=False)  # Keep for compatibility
    language = models.CharField(max_length=10, default='en')  # Keep for compatibility
    theme_preference = models.CharField(max_length=20, choices=[
        ('system', 'System'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    ], default='system')
    
    # Privacy Settings
    show_activity_status = models.BooleanField(default=True)
    show_artwork_stats = models.BooleanField(default=True)
    show_badges_publicly = models.BooleanField(default=True)
    
    # Account Status
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['level', '-total_xp']),
            models.Index(fields=['-artwork_created']),
            models.Index(fields=['-last_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize avatar if uploaded
        if self.avatar:
            self.resize_avatar()
        
        # Resize cover image if uploaded
        if self.cover_image:
            self.resize_cover()
    
    def resize_avatar(self):
        """Resize avatar to 300x300"""
        try:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
        except Exception as e:
            print(f"Error resizing avatar: {e}")
    
    def resize_cover(self):
        """Resize cover image to max 1200x400"""
        try:
            img = Image.open(self.cover_image.path)
            if img.height > 400 or img.width > 1200:
                # Maintain aspect ratio but limit dimensions
                ratio = min(1200/img.width, 400/img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img.save(self.cover_image.path)
        except Exception as e:
            print(f"Error resizing cover image: {e}")
    
    def add_xp(self, amount, reason=""):
        """Add XP and check for level up"""
        old_level = self.level
        self.total_xp += amount
        
        # Calculate new level (simple formula: level = sqrt(xp/100))
        import math
        new_level = max(1, int(math.sqrt(self.total_xp / 100)) + 1)
        
        if new_level > old_level:
            self.level = new_level
            self.save()
            
            # Create level up notification if gamification app is available
            try:
                from gamification.models import Notification
                Notification.objects.create(
                    recipient=self.user,
                    notification_type='level_up',
                    title=f'Level Up! You reached Level {new_level}',
                    message=f'Congratulations! You\'ve reached level {new_level}. Keep creating amazing art!'
                )
            except ImportError:
                pass
            
            return True  # Level up occurred
        else:
            self.save()
            return False  # No level up
    
    def get_next_level_xp(self):
        """Get XP required for next level"""
        next_level = self.level + 1
        required_xp = (next_level - 1) ** 2 * 100
        return max(0, required_xp - self.total_xp)
    
    def get_level_progress(self):
        """Get progress percentage to next level"""
        current_level_xp = (self.level - 1) ** 2 * 100
        next_level_xp = self.level ** 2 * 100
        
        if next_level_xp <= current_level_xp:
            return 100
        
        progress = ((self.total_xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100
        return max(0, min(100, progress))
    
    @property
    def display_name(self):
        """Return full name if available, otherwise username"""
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username
    
    @property
    def follower_count(self):
        """Get number of followers"""
        try:
            return self.user.followers.count()
        except:
            return 0
    
    @property
    def following_count(self):
        """Get number of users being followed"""
        try:
            return self.user.following.count()
        except:
            return 0
    
    @property
    def badge_count(self):
        """Get number of badges earned"""
        try:
            return self.user.user_badges.count()
        except:
            return 0

class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=200)
    search_type = models.CharField(max_length=20, choices=[
        ('artwork', 'Artwork'),
        ('artist', 'Artist'),
        ('tag', 'Tag'),
        ('general', 'General'),
    ], default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} searched for '{self.query}'"

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Display Preferences
    artworks_per_page = models.PositiveIntegerField(default=24)
    default_sort_order = models.CharField(max_length=20, choices=[
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('popular', 'Most Popular'),
        ('views', 'Most Viewed'),
        ('likes', 'Most Liked'),
    ], default='newest')
    
    # Content Filters
    hide_nsfw_content = models.BooleanField(default=True)
    hide_ai_generated = models.BooleanField(default=False)
    preferred_categories = models.JSONField(default=list, blank=True)
    blocked_tags = models.JSONField(default=list, blank=True)
    
    # Language and Locale
    language = models.CharField(max_length=10, choices=[
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('zh', 'Chinese'),
    ], default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserPreferences.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
    
    if hasattr(instance, 'preferences'):
        instance.preferences.save()
    else:
        UserPreferences.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Artwork(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='artworks/', max_length=500)  # Simplified path for Cloudinary
    thumbnail = models.ImageField(upload_to='artworks/thumbnails/', blank=True, max_length=500)  # Simplified path for Cloudinary
    
    # Relationships
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Metadata
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True, help_text="File size in bytes")
    
    # Engagement
    views = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['artist', '-created_at']),
            models.Index(fields=['visibility', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.artist.username}"
    
    def get_absolute_url(self):
        return reverse('gallery:artwork_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Create thumbnail if needed
        super().save(*args, **kwargs)
        
        if self.image and not self.thumbnail:
            self.create_thumbnail()
        
        # Update artist's artwork count
        self.artist.userprofile.artwork_created = self.artist.artworks.filter(visibility='public').count()
        self.artist.userprofile.save()
    
    def create_thumbnail(self):
        """Create a thumbnail for the artwork"""
        if not self.image:
            return
        
        try:
            # Open the image
            img = Image.open(self.image.path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Generate thumbnail path
            base_name = os.path.splitext(os.path.basename(self.image.name))[0]
            thumb_name = f"{base_name}_thumb.jpg"
            thumb_path = os.path.join('artworks/thumbnails', 
                                    self.created_at.strftime('%Y/%m/%d'), 
                                    thumb_name)
            
            # Save thumbnail
            full_thumb_path = os.path.join('media', thumb_path)
            os.makedirs(os.path.dirname(full_thumb_path), exist_ok=True)
            img.save(full_thumb_path, 'JPEG', quality=85, optimize=True)
            
            # Update thumbnail field
            self.thumbnail = thumb_path
            super().save(update_fields=['thumbnail'])
            
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

class ArtworkLike(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('artwork', 'user')
        indexes = [
            models.Index(fields=['artwork', 'user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.artwork.title}"

class ArtworkShare(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, blank=True)  # 'twitter', 'facebook', etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['artwork', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} shared {self.artwork.title}"

class ArtworkView(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='artwork_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['artwork', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} viewed {self.artwork.title}"
        return f"Anonymous viewed {self.artwork.title}"

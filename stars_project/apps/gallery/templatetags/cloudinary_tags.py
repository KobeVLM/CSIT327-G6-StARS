from django import template
from django.conf import settings
import re

register = template.Library()

@register.filter
def cloudinary_thumbnail(image_field, size="300x300"):
    """
    Generate a Cloudinary thumbnail URL with the specified size.
    Usage: {{ artwork.image|cloudinary_thumbnail:"150x150" }}
    """
    if not image_field:
        return ""
    
    # Check if we're using Cloudinary
    if hasattr(settings, 'CLOUDINARY_STORAGE') or 'cloudinary' in str(settings.STORAGES.get('default', {}).get('BACKEND', '')):
        image_url = str(image_field.url)
        
        # Clean up any duplicate cloudinary URLs
        if image_url.count('res.cloudinary.com') > 1:
            # Extract the clean path from the duplicated URL
            # From: https://res.cloudinary.com/.../https:/res.cloudinary.com/.../artworks/image.png
            # To: artworks/image.png
            parts = image_url.split('/')
            # Find the last occurrence of the actual file path
            if 'artworks' in image_url:
                artwork_index = -1
                for i, part in enumerate(parts):
                    if part == 'artworks':
                        artwork_index = i
                clean_path = '/'.join(parts[artwork_index:])
                image_url = f"https://res.cloudinary.com/dl3d6vid3/image/upload/{clean_path}"
        
        # If it's already a Cloudinary URL, add transformation
        if 'res.cloudinary.com' in image_url:
            # Insert transformation parameters
            width, height = size.split('x')
            return re.sub(
                r'(https://res\.cloudinary\.com/[^/]+/image/upload/)',
                rf'\1c_fill,w_{width},h_{height},q_auto,f_auto/',
                image_url
            )
    
    # Fallback to original URL for local development
    return image_field.url if image_field else ""

@register.filter
def cloudinary_url(image_field, transformations=""):
    """
    Generate a Cloudinary URL with custom transformations.
    Usage: {{ artwork.image|cloudinary_url:"c_fill,w_500,h_300,q_auto" }}
    """
    if not image_field:
        return ""
    
    # Check if we're using Cloudinary
    if hasattr(settings, 'CLOUDINARY_STORAGE') or 'cloudinary' in str(settings.STORAGES.get('default', {}).get('BACKEND', '')):
        image_url = str(image_field.url)
        
        # Clean up any duplicate cloudinary URLs
        if image_url.count('res.cloudinary.com') > 1:
            # Extract the clean path from the duplicated URL
            parts = image_url.split('/')
            if 'artworks' in image_url:
                artwork_index = -1
                for i, part in enumerate(parts):
                    if part == 'artworks':
                        artwork_index = i
                clean_path = '/'.join(parts[artwork_index:])
                image_url = f"https://res.cloudinary.com/dl3d6vid3/image/upload/{clean_path}"
        
        # If it's already a Cloudinary URL and transformations are provided
        if 'res.cloudinary.com' in image_url and transformations:
            return re.sub(
                r'(https://res\.cloudinary\.com/[^/]+/image/upload/)',
                rf'\1{transformations}/',
                image_url
            )
        elif 'res.cloudinary.com' in image_url:
            # Add basic optimization if no transformations specified
            return re.sub(
                r'(https://res\.cloudinary\.com/[^/]+/image/upload/)',
                r'\1q_auto,f_auto/',
                image_url
            )
    
    # Fallback to original URL
    return image_field.url if image_field else ""
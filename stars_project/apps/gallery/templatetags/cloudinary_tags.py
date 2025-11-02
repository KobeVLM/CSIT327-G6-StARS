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
        
        # If it's already a Cloudinary URL, add transformation
        if 'res.cloudinary.com' in image_url:
            # Insert transformation parameters
            # From: https://res.cloudinary.com/cloud_name/image/upload/v1234/image.jpg
            # To: https://res.cloudinary.com/cloud_name/image/upload/c_fill,w_300,h_300/v1234/image.jpg
            return re.sub(
                r'(https://res\.cloudinary\.com/[^/]+/image/upload/)',
                rf'\1c_fill,w_{size.split("x")[0]},h_{size.split("x")[1]}/',
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
        
        # If it's already a Cloudinary URL and transformations are provided
        if 'res.cloudinary.com' in image_url and transformations:
            return re.sub(
                r'(https://res\.cloudinary\.com/[^/]+/image/upload/)',
                rf'\1{transformations}/',
                image_url
            )
    
    # Fallback to original URL
    return image_field.url if image_field else ""
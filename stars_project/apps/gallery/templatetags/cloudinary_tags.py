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
        image_name = str(image_field.name) if hasattr(image_field, 'name') else str(image_field)
        
        # Handle various URL formats and extract the public ID
        public_id = image_name
        
        # If it's already a malformed URL, extract the public ID
        if 'res.cloudinary.com' in image_name:
            if 'artworks/' in image_name:
                # Extract everything after the last occurrence of 'artworks/'
                public_id = image_name.split('artworks/')[-1]
                public_id = f"artworks/{public_id}"
        
        # Clean up any remaining URL artifacts
        public_id = public_id.replace('https:/', '').replace('http:/', '')
        if public_id.startswith('/'):
            public_id = public_id[1:]
        
        # Construct proper Cloudinary URL with transformations
        width, height = size.split('x')
        return f"https://res.cloudinary.com/dl3d6vid3/image/upload/c_fill,w_{width},h_{height},q_auto,f_auto/{public_id}"
    
    # Fallback to original URL for local development
    return image_field.url if hasattr(image_field, 'url') else str(image_field)

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
        image_name = str(image_field.name) if hasattr(image_field, 'name') else str(image_field)
        
        # Handle various URL formats and extract the public ID
        public_id = image_name
        
        # If it's already a malformed URL, extract the public ID
        if 'res.cloudinary.com' in image_name:
            if 'artworks/' in image_name:
                # Extract everything after the last occurrence of 'artworks/'
                public_id = image_name.split('artworks/')[-1]
                public_id = f"artworks/{public_id}"
        
        # Clean up any remaining URL artifacts
        public_id = public_id.replace('https:/', '').replace('http:/', '')
        if public_id.startswith('/'):
            public_id = public_id[1:]
        
        # Construct proper Cloudinary URL
        if transformations:
            return f"https://res.cloudinary.com/dl3d6vid3/image/upload/{transformations}/{public_id}"
        else:
            return f"https://res.cloudinary.com/dl3d6vid3/image/upload/q_auto,f_auto/{public_id}"
    
    # Fallback to original URL
    return image_field.url if hasattr(image_field, 'url') else str(image_field)
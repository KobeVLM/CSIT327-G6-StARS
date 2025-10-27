# Example of enhanced Cloudinary usage (optional)
from cloudinary.models import CloudinaryField

class Artwork(models.Model):
    # Replace ImageField with CloudinaryField for more features
    # image = CloudinaryField('image', transformation=[
    #     {'quality': 'auto:good'},
    #     {'fetch_format': 'auto'}
    # ])
    
    # Or keep using ImageField - it will work with Cloudinary automatically
    image = models.ImageField(upload_to='artworks/%Y/%m/%d/')
from django.core.management.base import BaseCommand
from apps.gallery.models import Artwork

class Command(BaseCommand):
    help = 'Clean up duplicate Cloudinary URLs in thumbnails'
    
    def handle(self, *args, **options):
        # Find artworks with duplicate cloudinary URLs in thumbnails
        artworks_with_bad_thumbnails = Artwork.objects.filter(
            thumbnail__contains='https:/res.cloudinary.com/dl3d6vid3/image/upload/v'
        )
        
        self.stdout.write(f'Found {artworks_with_bad_thumbnails.count()} artworks with bad thumbnail URLs')
        
        for artwork in artworks_with_bad_thumbnails:
            self.stdout.write(f'Cleaning artwork: {artwork.title}')
            # Clear the bad thumbnail - we'll use the image with transformations instead
            artwork.thumbnail = None
            artwork.save()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully cleaned up thumbnail URLs!')
        )
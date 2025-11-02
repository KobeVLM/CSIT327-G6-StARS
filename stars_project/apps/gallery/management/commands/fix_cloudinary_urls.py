from django.core.management.base import BaseCommand
from apps.gallery.models import Artwork

class Command(BaseCommand):
    help = 'Fix corrupted Cloudinary URLs in the database'
    
    def handle(self, *args, **options):
        # Find artworks with corrupted URLs
        corrupted_artworks = Artwork.objects.filter(
            image__contains='https:/res.cloudinary.com'
        )
        
        self.stdout.write(f'Found {corrupted_artworks.count()} artworks with corrupted URLs')
        
        for artwork in corrupted_artworks:
            self.stdout.write(f'Fixing artwork: {artwork.title}')
            
            # Extract the clean Cloudinary public ID from the corrupted URL
            # From: https:/res.cloudinary.com/dl3d6vid3/artworks/2_ojfang
            # To: artworks/2_ojfang
            if 'artworks/' in artwork.image.name:
                # Extract the part after "artworks/"
                parts = artwork.image.name.split('artworks/')
                if len(parts) > 1:
                    clean_public_id = f"artworks/{parts[-1]}"
                    
                    # Update the field with just the public ID
                    artwork.image.name = clean_public_id
                    artwork.thumbnail.name = clean_public_id if artwork.thumbnail else None
                    
                    artwork.save()
                    self.stdout.write(f'  Fixed to: {clean_public_id}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully fixed corrupted URLs!')
        )
from django.core.management.base import BaseCommand
from apps.gallery.models import Category, Tag

class Command(BaseCommand):
    help = 'Create sample categories and tags for the gallery'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Digital Art', 'slug': 'digital-art', 'description': 'Art created using digital tools'},
            {'name': 'Traditional Art', 'slug': 'traditional-art', 'description': 'Hand-drawn and painted artwork'},
            {'name': 'Photography', 'slug': 'photography', 'description': 'Photographic artwork'},
            {'name': 'Illustration', 'slug': 'illustration', 'description': 'Illustrative artwork'},
            {'name': 'Concept Art', 'slug': 'concept-art', 'description': 'Concept and design artwork'},
            {'name': 'Fan Art', 'slug': 'fan-art', 'description': 'Fan-based artwork'},
            {'name': '3D Art', 'slug': '3d-art', 'description': '3D rendered artwork'},
            {'name': 'Pixel Art', 'slug': 'pixel-art', 'description': 'Pixel-based artwork'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create tags
        tags_data = [
            'portrait', 'landscape', 'fantasy', 'sci-fi', 'anime', 'manga',
            'realistic', 'abstract', 'cartoon', 'character-design',
            'environment', 'creature', 'vehicle', 'weapon', 'armor',
            'magic', 'dragon', 'warrior', 'princess', 'robot',
            'cyberpunk', 'steampunk', 'medieval', 'futuristic',
            'dark', 'bright', 'colorful', 'monochrome', 'sketch',
            'painting', 'drawing', 'digital-painting', 'photoshop',
            'procreate', 'krita', 'blender', 'maya', 'zbrush'
        ]
        
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample categories and tags!')
        )
from django.core.management.base import BaseCommand
from apps.gamification.models import Badge

class Command(BaseCommand):
    help = 'Create sample badges for the gamification system'
    
    def handle(self, *args, **options):
        # Create badges data
        badges_data = [
            # Upload Badges
            {
                'name': 'First Upload',
                'description': 'Upload your first artwork to the platform',
                'icon': 'upload',
                'badge_type': 'upload',
                'requirement_value': 1,
                'xp_reward': 50,
                'rarity': 'common'
            },
            {
                'name': 'Prolific Creator',
                'description': 'Upload 10 artworks',
                'icon': 'image',
                'badge_type': 'upload',
                'requirement_value': 10,
                'xp_reward': 200,
                'rarity': 'rare'
            },
            {
                'name': 'Art Gallery',
                'description': 'Upload 50 artworks',
                'icon': 'gallery-horizontal',
                'badge_type': 'upload',
                'requirement_value': 50,
                'xp_reward': 500,
                'rarity': 'epic'
            },
            {
                'name': 'Master Artist',
                'description': 'Upload 100 artworks',
                'icon': 'crown',
                'badge_type': 'upload',
                'requirement_value': 100,
                'xp_reward': 1000,
                'rarity': 'legendary'
            },
            
            # Engagement Badges
            {
                'name': 'Well Liked',
                'description': 'Receive 10 likes on your artwork',
                'icon': 'heart',
                'badge_type': 'engagement',
                'requirement_value': 10,
                'xp_reward': 100,
                'rarity': 'common'
            },
            {
                'name': 'Popular Artist',
                'description': 'Receive 100 likes on your artwork',
                'icon': 'star',
                'badge_type': 'engagement',
                'requirement_value': 100,
                'xp_reward': 300,
                'rarity': 'rare'
            },
            {
                'name': 'Community Favorite',
                'description': 'Receive 500 likes on your artwork',
                'icon': 'sparkles',
                'badge_type': 'engagement',
                'requirement_value': 500,
                'xp_reward': 750,
                'rarity': 'epic'
            },
            {
                'name': 'Viral Artist',
                'description': 'Receive 1000 likes on your artwork',
                'icon': 'zap',
                'badge_type': 'engagement',
                'requirement_value': 1000,
                'xp_reward': 1500,
                'rarity': 'legendary'
            },
            
            # Milestone Badges
            {
                'name': 'Apprentice',
                'description': 'Reach Level 5',
                'icon': 'graduation-cap',
                'badge_type': 'milestone',
                'requirement_value': 5,
                'xp_reward': 250,
                'rarity': 'common'
            },
            {
                'name': 'Artist',
                'description': 'Reach Level 10',
                'icon': 'palette',
                'badge_type': 'milestone',
                'requirement_value': 10,
                'xp_reward': 500,
                'rarity': 'rare'
            },
            {
                'name': 'Expert',
                'description': 'Reach Level 25',
                'icon': 'trophy',
                'badge_type': 'milestone',
                'requirement_value': 25,
                'xp_reward': 1000,
                'rarity': 'epic'
            },
            {
                'name': 'Legendary',
                'description': 'Reach Level 50',
                'icon': 'crown',
                'badge_type': 'milestone',
                'requirement_value': 50,
                'xp_reward': 2500,
                'rarity': 'legendary'
            },
            
            # Special Badges
            {
                'name': 'Early Adopter',
                'description': 'One of the first users to join STARS',
                'icon': 'rocket',
                'badge_type': 'special',
                'requirement_value': 1,
                'xp_reward': 100,
                'rarity': 'epic'
            },
            {
                'name': 'Profile Complete',
                'description': 'Complete your profile with all information',
                'icon': 'check-circle',
                'badge_type': 'special',
                'requirement_value': 1,
                'xp_reward': 75,
                'rarity': 'common'
            },
            {
                'name': 'Social Butterfly',
                'description': 'Connect all your social media accounts',
                'icon': 'share-2',
                'badge_type': 'special',
                'requirement_value': 1,
                'xp_reward': 150,
                'rarity': 'rare'
            },
        ]
        
        created_count = 0
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created badge: {badge.name} ({badge.rarity})')
                )
            else:
                self.stdout.write(f'Badge already exists: {badge.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new badges!')
        )
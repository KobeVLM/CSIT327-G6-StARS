from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.gamification.models import Badge, UserBadge
from apps.gamification.utils import check_and_award_badges

class Command(BaseCommand):
    help = 'Test badge earning functionality for a specific user'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to test badges for')
        parser.add_argument('--award-all', action='store_true', help='Award all available badges to the user')
        parser.add_argument('--reset', action='store_true', help='Remove all badges from the user')
    
    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
            return
        
        if options['reset']:
            # Remove all badges from user
            deleted_count = UserBadge.objects.filter(user=user).count()
            UserBadge.objects.filter(user=user).delete()
            self.stdout.write(self.style.SUCCESS(f'Removed {deleted_count} badges from {username}'))
            return
        
        if options['award_all']:
            # Award all badges to user (for testing purposes)
            all_badges = Badge.objects.filter(is_active=True)
            awarded_count = 0
            
            for badge in all_badges:
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=badge
                )
                if created:
                    awarded_count += 1
                    self.stdout.write(f'Awarded: {badge.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Awarded {awarded_count} new badges to {username}'))
            return
        
        # Show current user stats and badges
        profile = user.userprofile
        
        self.stdout.write(f'\n=== User Stats for {username} ===')
        self.stdout.write(f'Level: {profile.level}')
        self.stdout.write(f'Total XP: {profile.total_xp}')
        self.stdout.write(f'Artwork Created: {profile.artwork_created}')
        self.stdout.write(f'Total Likes Received: {profile.total_likes_received}')
        
        # Show earned badges
        earned_badges = UserBadge.objects.filter(user=user).select_related('badge')
        self.stdout.write(f'\n=== Earned Badges ({earned_badges.count()}) ===')
        for user_badge in earned_badges:
            self.stdout.write(f'✅ {user_badge.badge.name} - {user_badge.badge.rarity}')
        
        # Show available badges (not earned yet)
        earned_badge_ids = earned_badges.values_list('badge_id', flat=True)
        available_badges = Badge.objects.filter(is_active=True).exclude(id__in=earned_badge_ids)
        
        self.stdout.write(f'\n=== Available Badges ({available_badges.count()}) ===')
        for badge in available_badges:
            progress = self.calculate_progress(user, badge)
            progress_text = f'{progress["current"]}/{progress["required"]}' if progress["required"] > 0 else 'Special'
            self.stdout.write(f'⏳ {badge.name} - {badge.rarity} ({progress_text})')
        
        # Test badge checking
        self.stdout.write(f'\n=== Testing Badge Awards ===')
        try:
            check_and_award_badges(user)
            self.stdout.write('✅ Badge check completed successfully')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Badge check failed: {e}'))
    
    def calculate_progress(self, user, badge):
        """Calculate progress towards earning a specific badge"""
        profile = user.userprofile
        
        if badge.badge_type == 'upload':
            current = profile.artwork_created
            required = badge.requirement_value
        elif badge.badge_type == 'engagement':
            current = profile.total_likes_received
            required = badge.requirement_value
        elif badge.badge_type == 'milestone':
            current = profile.level
            required = badge.requirement_value
        else:  # special badges
            current = 0
            required = badge.requirement_value
        
        return {
            'current': current,
            'required': required,
            'percentage': (current / required * 100) if required > 0 else 0
        }
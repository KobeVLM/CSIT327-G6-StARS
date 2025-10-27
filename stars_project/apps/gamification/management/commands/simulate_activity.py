from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.gamification.utils import award_upload_xp, award_like_xp

class Command(BaseCommand):
    help = 'Simulate user activity to test badge earning'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to simulate activity for')
        parser.add_argument('--uploads', type=int, default=0, help='Number of uploads to simulate')
        parser.add_argument('--likes', type=int, default=0, help='Number of likes to simulate')
        parser.add_argument('--level-up', action='store_true', help='Add enough XP to level up')
    
    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
            return
        
        profile = user.userprofile
        
        self.stdout.write(f'\n=== Before Simulation ===')
        self.stdout.write(f'Level: {profile.level}, XP: {profile.total_xp}')
        self.stdout.write(f'Uploads: {profile.artwork_created}, Likes: {profile.total_likes_received}')
        
        # Simulate uploads
        if options['uploads'] > 0:
            self.stdout.write(f'\n🎨 Simulating {options["uploads"]} uploads...')
            for i in range(options['uploads']):
                xp_gained = award_upload_xp(user)
                self.stdout.write(f'Upload {i+1}: +{xp_gained} XP')
        
        # Simulate likes
        if options['likes'] > 0:
            self.stdout.write(f'\n❤️ Simulating {options["likes"]} likes...')
            for i in range(options['likes']):
                xp_gained = award_like_xp(user)
                self.stdout.write(f'Like {i+1}: +{xp_gained} XP')
        
        # Level up simulation
        if options['level_up']:
            self.stdout.write(f'\n🚀 Adding XP for level up...')
            # Calculate XP needed for next level
            next_level = profile.level + 1
            required_xp = (next_level - 1) ** 2 * 100
            current_xp = profile.total_xp
            xp_needed = max(0, required_xp - current_xp + 1)
            
            if xp_needed > 0:
                profile.add_xp(xp_needed, "Manual level up simulation")
                self.stdout.write(f'Added {xp_needed} XP for level up')
            else:
                self.stdout.write('User already has enough XP for next level')
        
        # Refresh profile
        profile.refresh_from_db()
        
        self.stdout.write(f'\n=== After Simulation ===')
        self.stdout.write(f'Level: {profile.level}, XP: {profile.total_xp}')
        self.stdout.write(f'Uploads: {profile.artwork_created}, Likes: {profile.total_likes_received}')
        
        # Show newly earned badges
        from gamification.models import UserBadge
        recent_badges = UserBadge.objects.filter(user=user).order_by('-earned_at')[:5]
        
        if recent_badges:
            self.stdout.write(f'\n🏆 Recent Badges:')
            for user_badge in recent_badges:
                self.stdout.write(f'  • {user_badge.badge.name} ({user_badge.badge.rarity})')
        
        self.stdout.write(f'\n✅ Simulation complete! Check badges at: http://127.0.0.1:8000/gamification/badges/')
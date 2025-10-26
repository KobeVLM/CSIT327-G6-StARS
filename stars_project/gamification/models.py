from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Badge(models.Model):
    BADGE_TYPES = [
        ('upload', 'Upload Achievement'),
        ('engagement', 'Engagement Achievement'),
        ('milestone', 'Milestone Achievement'),
        ('special', 'Special Achievement'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Lucide icon name")
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    requirement_value = models.PositiveIntegerField(help_text="Required value to earn badge")
    xp_reward = models.PositiveIntegerField(default=0)
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ], default='common')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['badge_type', 'requirement_value']
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"

class XPTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('artwork_upload', 'Artwork Upload'),
        ('artwork_like', 'Artwork Like Received'),
        ('artwork_share', 'Artwork Share'),
        ('profile_complete', 'Profile Completion'),
        ('badge_earned', 'Badge Earned'),
        ('daily_login', 'Daily Login'),
        ('contest_win', 'Contest Win'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_transactions')
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    xp_amount = models.IntegerField()  # Can be negative
    description = models.CharField(max_length=200)
    
    # Generic relation to link to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.xp_amount} XP for {self.description}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Artwork Liked'),
        ('share', 'Artwork Shared'),
        ('follow', 'New Follower'),
        ('badge', 'Badge Earned'),
        ('level_up', 'Level Up'),
        ('contest', 'Contest Notification'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Generic relation to link to any model (artwork, badge, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
            models.Index(fields=['recipient', 'notification_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = models.timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

class UserFollowing(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Contest(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('judging', 'Judging'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    theme = models.CharField(max_length=100, blank=True)
    
    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    judging_end_date = models.DateTimeField()
    
    # Prizes
    first_prize_xp = models.PositiveIntegerField(default=1000)
    second_prize_xp = models.PositiveIntegerField(default=500)
    third_prize_xp = models.PositiveIntegerField(default=250)
    participation_xp = models.PositiveIntegerField(default=50)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title

class ContestSubmission(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='submissions')
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey('gallery.Artwork', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('contest', 'participant')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.participant.username} - {self.contest.title}"

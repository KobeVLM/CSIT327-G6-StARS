from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 🏆 Reward - Logs user achievements, experience, or points (N:1 → User)
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reason}"

    class Meta:
        ordering = ['-date_awarded']

# 🎖️ Badge - Represents gamification milestones (N:M → User via UserBadge)
class Badge(models.Model):
    badge_name = models.CharField(max_length=100)
    description = models.TextField()
    level_required = models.IntegerField()

    def __str__(self):
        return self.badge_name

# 🧍‍♂️ UserBadge - Junction table for user–badge achievements (N:1 → User, N:1 → Badge)
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    date_earned = models.DateTimeField(auto_now_add=True)
    level_required = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.badge_name}"

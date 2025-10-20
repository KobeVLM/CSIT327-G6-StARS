from django.db import models
from django.contrib.auth.models import User
from apps.gallery.models import Post

# Create your models here.

# 🛡️ Moderation - Tracks admin actions (N:1 → User as admin, N:1 → Post optional, N:1 → User optional target)
class Moderation(models.Model):
    admin = models.ForeignKey(User, related_name='moderation_actions', on_delete=models.CASCADE)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, related_name='moderation_targets', on_delete=models.CASCADE, null=True, blank=True)
    action_taken = models.CharField(max_length=100)
    reason = models.TextField()
    date_actioned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Moderation by {self.admin.username} - {self.action_taken}"

    class Meta:
        ordering = ['-date_actioned']

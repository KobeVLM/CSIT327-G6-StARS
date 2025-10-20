from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 🧑‍🎨 Profile - Holds extended user details (1:1 → User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# ⚙️ Settings - Stores user preferences (1:1 → User)
class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    notifications_enabled = models.BooleanField(default=True)
    level_required = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Settings"

    class Meta:
        verbose_name_plural = "Settings"

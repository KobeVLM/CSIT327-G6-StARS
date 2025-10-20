from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True, unique=True)
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    file_url = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=20)
    upload_date = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ])

    tags = models.ManyToManyField(Tag, through='PostTag')

    def __str__(self):
        return self.title

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now_add=True)


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    share_date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Badge(models.Model):
    badge_name = models.CharField(max_length=100)
    description = models.TextField()
    level_required = models.IntegerField()

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)


class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    date_awarded = models.DateTimeField(auto_now_add=True)


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=True)
    level_required = models.IntegerField(default=1)


class Moderation(models.Model):
    admin = models.ForeignKey(User, related_name='moderator', on_delete=models.CASCADE)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='reported_user', on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=100)
    reason = models.TextField()
    date_actioned = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 🏷️ Category - Classifies posts into types (1:N → Post)
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"

# 🏷️ Tag - Provides keyword-style labels for posts (N:M → Post via PostTag)
class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name

# 🖼️ Post - Stores uploaded artwork (N:1 → User, N:1 → Category, N:M → Tag)
class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    file_url = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=20)
    upload_date = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    tags = models.ManyToManyField(Tag, through='PostTag', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

# 🔗 PostTag - Junction table linking posts and tags (N:1 → Post, N:1 → Tag)
class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post', 'tag')

# ❤️ Like - Tracks which users like which posts (N:1 → User, N:1 → Post)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date_liked = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')

# 🔁 Share - Records when users share a post (N:1 → User, N:1 → Post)
class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    share_date = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} shared {self.post.title}"

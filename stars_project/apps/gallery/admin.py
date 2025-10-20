from django.contrib import admin
from .models import Category, Tag, Post, PostTag, Like, Share

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'visibility', 'upload_date')
    list_filter = ('category', 'visibility', 'upload_date')
    search_fields = ('title', 'user__username')

@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ('post', 'tag')
    list_filter = ('tag',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_liked')
    list_filter = ('date_liked',)

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'platform', 'share_date')
    list_filter = ('platform', 'share_date')

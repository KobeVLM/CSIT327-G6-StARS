from django.contrib import admin
from .models import Badge, UserBadge, Reward

# Register your models here.

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('badge_name', 'level_required')
    search_fields = ('badge_name',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'date_earned', 'level_required')
    list_filter = ('date_earned', 'level_required')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'exp', 'reason', 'date_awarded')
    list_filter = ('date_awarded',)

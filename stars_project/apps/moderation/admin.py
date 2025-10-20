from django.contrib import admin
from .models import Moderation

# Register your models here.

@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_taken', 'target_post', 'target_user', 'date_actioned')
    list_filter = ('action_taken', 'date_actioned')
    search_fields = ('admin__username', 'reason')

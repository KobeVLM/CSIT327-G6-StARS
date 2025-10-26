from django.db import models
from django.contrib.auth.models import User
from gallery.models import Artwork

class Report(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('copyright', 'Copyright Violation'),
        ('harassment', 'Harassment'),
        ('violence', 'Violence'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('dismissed', 'Dismissed'),
    ]
    
    # Report details
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('artwork', 'reported_by')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report #{self.id} - {self.artwork.title} by {self.reported_by.username}"

class UserViolation(models.Model):
    VIOLATION_TYPES = [
        ('content', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('copyright', 'Copyright Violation'),
        ('other', 'Other'),
    ]
    
    ACTION_TYPES = [
        ('warning', 'Warning'),
        ('suspend', 'Suspended'),
        ('ban', 'Banned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=20, choices=VIOLATION_TYPES)
    description = models.TextField()
    
    # Related report (optional)
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Action taken
    action_taken = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Admin who took action
    actioned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_actions')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Violation - {self.user.username} ({self.violation_type})"

class ModerationSettings(models.Model):
    # Auto-moderation settings
    auto_hide_reported_content = models.BooleanField(default=False)
    reports_threshold_hide = models.PositiveIntegerField(default=5)
    
    # Notification settings
    notify_admins_new_report = models.BooleanField(default=True)
    notify_users_action_taken = models.BooleanField(default=True)
    
    # Content filtering
    enable_profanity_filter = models.BooleanField(default=True)
    require_approval_new_users = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Moderation Settings"
        verbose_name_plural = "Moderation Settings"
    
    def __str__(self):
        return "Moderation Settings"

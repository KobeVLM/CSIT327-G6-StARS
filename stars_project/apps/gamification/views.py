from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification, Badge, UserBadge

@login_required
def badges(request):
    """Display user badges and available badges"""
    user_profile = request.user.userprofile
    
    # Get earned badges
    earned_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    earned_badge_ids = earned_badges.values_list('badge_id', flat=True)
    
    # Get available badges (not earned yet)
    available_badges = Badge.objects.filter(is_active=True).exclude(id__in=earned_badge_ids)
    
    # Add progress calculation for available badges
    available_badges_with_progress = []
    for badge in available_badges:
        progress_data = calculate_badge_progress(request.user, badge)
        available_badges_with_progress.append({
            'badge': badge,
            'progress_percentage': progress_data['percentage'],
            'current_value': progress_data['current'],
            'required_value': progress_data['required'],
            'level_required': badge.requirement_value if badge.badge_type == 'milestone' else None,
        })
    
    # Level progress calculation
    level_progress = user_profile.get_level_progress()
    xp_to_next_level = user_profile.get_next_level_xp()
    
    context = {
        'earned_badges': earned_badges,
        'available_badges': available_badges_with_progress,
        'earned_badges_count': earned_badges.count(),
        'available_badges_count': available_badges.count(),
        'profile': user_profile,
        'level_progress': level_progress,
        'xp_to_next_level': xp_to_next_level,
    }
    return render(request, 'gamification/badges.html', context)

def calculate_badge_progress(user, badge):
    """Calculate progress towards earning a specific badge"""
    user_profile = user.userprofile
    
    if badge.badge_type == 'upload':
        current = user_profile.artwork_created
        required = badge.requirement_value
    elif badge.badge_type == 'engagement':
        current = user_profile.total_likes_received
        required = badge.requirement_value
    elif badge.badge_type == 'milestone':
        current = user_profile.level
        required = badge.requirement_value
    else:
        current = 0
        required = badge.requirement_value
    
    percentage = min(100, (current / required * 100)) if required > 0 else 0
    
    return {
        'current': current,
        'required': required,
        'percentage': round(percentage, 1)
    }

@login_required
def notifications(request):
    """Display user notifications with filtering"""
    notifications_qs = Notification.objects.filter(
        recipient=request.user,
        is_deleted=False
    ).select_related('sender').order_by('-created_at')
    
    # Filter by type
    filter_type = request.GET.get('filter')
    if filter_type == 'unread':
        notifications_qs = notifications_qs.filter(is_read=False)
    elif filter_type in ['like', 'share', 'follow', 'badge', 'level_up', 'contest', 'system']:
        notifications_qs = notifications_qs.filter(notification_type=filter_type)
    
    # Pagination
    paginator = Paginator(notifications_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Counts
    total_count = Notification.objects.filter(recipient=request.user, is_deleted=False).count()
    unread_count = Notification.objects.filter(recipient=request.user, is_deleted=False, is_read=False).count()
    
    context = {
        'notifications': page_obj,
        'filter_type': filter_type,
        'total_count': total_count,
        'unread_count': unread_count,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'gamification/notifications.html', context)

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.mark_as_read()
    messages.success(request, 'Notification marked as read.')
    return redirect('gamification:notifications')

@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_deleted=False
    ).update(is_read=True)
    
    messages.success(request, f'Marked {count} notifications as read.')
    return redirect('gamification:notifications')

@login_required
@require_POST
def delete_notification(request, notification_id):
    """Delete a notification"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.is_deleted = True
    notification.save()
    messages.success(request, 'Notification deleted.')
    return redirect('gamification:notifications')

@login_required
def badges(request):
    """Display user badges and available badges"""
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge').order_by('-earned_at')
    available_badges = Badge.objects.filter(is_active=True).order_by('badge_type', 'requirement_value')
    
    # Get earned badge IDs for filtering
    earned_badge_ids = user_badges.values_list('badge_id', flat=True)
    unearned_badges = available_badges.exclude(id__in=earned_badge_ids)
    
    context = {
        'user_badges': user_badges,
        'available_badges': available_badges,
        'unearned_badges': unearned_badges,
        'earned_count': user_badges.count(),
        'total_count': available_badges.count(),
    }
    return render(request, 'gamification/badges.html', context)

def leaderboard(request):
    """Display leaderboard of top users"""
    from django.contrib.auth.models import User
    from django.db.models import Q
    
    # Get top users by XP
    top_users = User.objects.select_related('userprofile').filter(
        userprofile__is_profile_public=True
    ).order_by('-userprofile__total_xp', '-userprofile__level')[:100]
    
    # Find current user's rank if authenticated
    user_rank = None
    if request.user.is_authenticated:
        users_with_higher_xp = User.objects.filter(
            userprofile__total_xp__gt=request.user.userprofile.total_xp
        ).count()
        user_rank = users_with_higher_xp + 1
    
    context = {
        'top_users': top_users,
        'user_rank': user_rank,
    }
    return render(request, 'gamification/leaderboard.html', context)

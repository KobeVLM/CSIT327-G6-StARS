from .models import Badge, UserBadge, XPTransaction, Notification
from django.contrib.auth.models import User

def check_and_award_badges(user):
    """Check if user qualifies for any new badges and award them"""
    profile = user.userprofile
    earned_badge_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    available_badges = Badge.objects.filter(is_active=True).exclude(id__in=earned_badge_ids)
    
    newly_awarded = []
    
    for badge in available_badges:
        if should_award_badge(user, badge):
            # Award the badge
            user_badge = UserBadge.objects.create(user=user, badge=badge)
            
            # Award XP
            if badge.xp_reward > 0:
                profile.add_xp(badge.xp_reward, f"Earned badge: {badge.name}")
            
            # Create notification
            try:
                Notification.objects.create(
                    recipient=user,
                    notification_type='badge_earned',
                    title=f'Badge Earned: {badge.name}',
                    message=f'Congratulations! You\'ve earned the "{badge.name}" badge. +{badge.xp_reward} XP!'
                )
            except Exception:
                pass  # Continue even if notification fails
            
            newly_awarded.append(badge)
    
    return newly_awarded

def should_award_badge(user, badge):
    """Check if user qualifies for a specific badge"""
    profile = user.userprofile
    
    if badge.badge_type == 'upload':
        return profile.artwork_created >= badge.requirement_value
    elif badge.badge_type == 'engagement':
        return profile.total_likes_received >= badge.requirement_value
    elif badge.badge_type == 'milestone':
        return profile.level >= badge.requirement_value
    elif badge.badge_type == 'special':
        # Special badges need custom logic
        if badge.name == 'Profile Complete':
            return is_profile_complete(user)
        elif badge.name == 'Social Butterfly':
            return has_all_social_links(user)
        elif badge.name == 'Early Adopter':
            # Could check join date or user ID
            return user.id <= 100  # First 100 users
    
    return False

def is_profile_complete(user):
    """Check if user profile is complete"""
    profile = user.userprofile
    required_fields = [
        profile.bio,
        user.first_name,
        user.last_name,
    ]
    return all(field.strip() for field in required_fields if field)

def has_all_social_links(user):
    """Check if user has connected all social media accounts"""
    profile = user.userprofile
    social_links = [
        profile.instagram_url,
        profile.twitter_url,
        profile.behance_url,
        profile.dribbble_url,
    ]
    # User needs at least 3 social links filled
    filled_links = [link for link in social_links if link.strip()]
    return len(filled_links) >= 3

def award_upload_xp(user, artwork=None):
    """Award XP for uploading artwork"""
    xp_amount = 25  # Base XP for upload
    user.userprofile.add_xp(xp_amount, "Artwork upload")
    
    # Increment artwork count
    user.userprofile.artwork_created += 1
    user.userprofile.save()
    
    # Check for new badges
    check_and_award_badges(user)
    
    return xp_amount

def award_like_xp(user, artwork=None):
    """Award XP for receiving a like"""
    xp_amount = 5  # Base XP for receiving a like
    user.userprofile.add_xp(xp_amount, "Artwork liked")
    
    # Increment likes received count
    user.userprofile.total_likes_received += 1
    user.userprofile.save()
    
    # Check for new badges
    check_and_award_badges(user)
    
    return xp_amount
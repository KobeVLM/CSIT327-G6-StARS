from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Report, UserViolation, ModerationSettings
from apps.gallery.models import Artwork

def is_staff_or_admin(user):
    """Check if user is staff or admin"""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_admin)
def moderation_dashboard(request):
    """Main moderation dashboard"""
    # Get pending reports
    pending_reports = Report.objects.filter(status='pending').select_related(
        'artwork', 'reported_by', 'artwork__artist'
    ).order_by('-created_at')
    
    # Get flagged users (users with violations)
    flagged_users = User.objects.annotate(
        violation_count=Count('violations')
    ).filter(violation_count__gt=0).order_by('-violation_count')
    
    # Add violation details to flagged users
    for user in flagged_users:
        user.violations_data = user.violations.all()[:3]  # Latest 3 violations
        user.latest_violation = user.violations.first()
    
    context = {
        'pending_reports': pending_reports,
        'flagged_users': flagged_users,
        'reports_count': pending_reports.count(),
        'flagged_users_count': flagged_users.count(),
    }
    
    return render(request, 'moderation/dashboard.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def delete_artwork(request, artwork_id):
    """Delete reported artwork"""
    artwork = get_object_or_404(Artwork, id=artwork_id)
    
    # Update related reports
    reports = Report.objects.filter(artwork=artwork, status='pending')
    reports.update(
        status='approved',
        reviewed_by=request.user,
        reviewed_at=timezone.now()
    )
    
    # Create violation record for the artist
    UserViolation.objects.create(
        user=artwork.artist,
        violation_type='content',
        description=f'Artwork "{artwork.title}" was deleted due to violations',
        action_taken='warning',
        actioned_by=request.user
    )
    
    artwork_title = artwork.title
    artwork.delete()
    
    messages.success(request, f'Artwork "{artwork_title}" has been deleted successfully.')
    return JsonResponse({'status': 'success', 'message': f'Artwork "{artwork_title}" has been deleted'})

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def dismiss_report(request, report_id):
    """Dismiss a report"""
    report = get_object_or_404(Report, id=report_id)
    
    report.status = 'dismissed'
    report.reviewed_by = request.user
    report.reviewed_at = timezone.now()
    report.save()
    
    messages.success(request, f'Report #{report.id} has been dismissed.')
    return JsonResponse({'status': 'success', 'message': 'Report has been dismissed'})

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def suspend_user(request, user_id):
    """Suspend a user"""
    user = get_object_or_404(User, id=user_id)
    
    # Set user as inactive (suspended)
    user.is_active = False
    user.save()
    
    # Create violation record
    UserViolation.objects.create(
        user=user,
        violation_type='other',
        description='User suspended by moderator',
        action_taken='suspend',
        actioned_by=request.user
    )
    
    messages.success(request, f'User {user.username} has been suspended.')
    return JsonResponse({'status': 'success', 'message': f'User {user.username} has been suspended'})

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def activate_user(request, user_id):
    """Reactivate a suspended user"""
    user = get_object_or_404(User, id=user_id)
    
    user.is_active = True
    user.save()
    
    messages.success(request, f'User {user.username} has been reactivated.')
    return JsonResponse({'status': 'success', 'message': f'User {user.username} has been reactivated'})

@login_required
@user_passes_test(is_staff_or_admin)
def report_artwork(request, artwork_id):
    """Report an artwork (admin can also create reports)"""
    artwork = get_object_or_404(Artwork, id=artwork_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        # Check if user already reported this artwork
        existing_report = Report.objects.filter(
            artwork=artwork,
            reported_by=request.user
        ).first()
        
        if existing_report:
            messages.warning(request, 'You have already reported this artwork.')
        else:
            Report.objects.create(
                artwork=artwork,
                reported_by=request.user,
                reason=reason,
                description=description
            )
            messages.success(request, 'Report submitted successfully.')
        
        return redirect('moderation:dashboard')
    
    context = {
        'artwork': artwork,
        'report_reasons': Report.REPORT_REASONS,
    }
    
    return render(request, 'moderation/report_form.html', context)

@login_required
@require_POST
def submit_report(request):
    """Submit a report for an artwork via AJAX"""
    artwork_id = request.POST.get('artwork_id')
    reason = request.POST.get('reason')
    description = request.POST.get('description', '')
    
    try:
        artwork = get_object_or_404(Artwork, id=artwork_id)
        
        # Check if user already reported this artwork
        existing_report = Report.objects.filter(
            artwork=artwork,
            reported_by=request.user
        ).first()
        
        if existing_report:
            return JsonResponse({
                'success': False, 
                'message': 'You have already reported this artwork.'
            })
        
        # Check if user is trying to report their own artwork
        if artwork.artist == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'You cannot report your own artwork.'
            })
        
        # Create the report
        Report.objects.create(
            artwork=artwork,
            reported_by=request.user,
            reason=reason,
            description=description
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Report submitted successfully. Our moderation team will review it shortly.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'An error occurred while submitting your report.'
        })

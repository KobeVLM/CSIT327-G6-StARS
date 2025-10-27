def user_profile_context(request):
    """Add user profile to template context if user is authenticated"""
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        context['profile'] = request.user.userprofile
    return context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('gallery:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username or email
        user = authenticate(request, username=username, password=password)
        if not user:
            # Try with email
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            return redirect('gallery:dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'auth/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('gallery:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')
        
        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif not email.endswith('@gmail.com'):
            messages.error(request, 'Please use a Gmail address.')
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            if full_name:
                user.first_name = full_name.split()[0] if full_name.split() else ''
                user.last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                user.save()
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('users:login')
    
    return render(request, 'auth/register.html')

@login_required
def profile_view(request):
    profile = request.user.userprofile
    
    if request.method == 'POST':
        # Handle profile updates via AJAX or form submission
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        website = request.POST.get('website', '')
        
        profile.bio = bio
        profile.location = location
        profile.website = website
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    return render(request, 'users/profile.html', {'profile': profile})

def profile_detail(request, username):
    """View for viewing other users' public profiles"""
    user = get_object_or_404(User, username=username)
    profile = user.userprofile
    
    # Check if profile is public
    if not profile.is_profile_public and request.user != user:
        messages.error(request, 'This profile is private.')
        return redirect('gallery:browse')
    
    # Get user's artworks
    try:
        from gallery.models import Artwork
        artworks = Artwork.objects.filter(
            artist=user, 
            visibility='public'
        ).order_by('-created_at')[:12]
    except ImportError:
        artworks = []
    
    context = {
        'profile_user': user,
        'profile': profile,
        'artworks': artworks,
        'is_own_profile': request.user == user,
    }
    return render(request, 'users/profile_detail.html', context)

@login_required
def settings_view(request):
    profile = request.user.userprofile
    
    if request.method == 'POST':
        # Handle settings updates
        profile.dark_mode = request.POST.get('dark_mode') == 'on'
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.push_notifications = request.POST.get('push_notifications') == 'on'
        profile.language = request.POST.get('language', 'en')
        
        # Handle bio, location, website updates
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        website = request.POST.get('website', '').strip()
        
        if bio:
            profile.bio = bio
        if location:
            profile.location = location
        if website:
            profile.website = website
            
        # Update user's full name if provided
        display_name = request.POST.get('display_name', '').strip()
        if display_name:
            name_parts = display_name.split(' ', 1)
            request.user.first_name = name_parts[0]
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            request.user.save()
        
        profile.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('users:settings')
    
    return render(request, 'users/settings.html', {'profile': profile})

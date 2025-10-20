from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Profile, Settings

# Create your models here.

# User Authentication Views

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('users:landing')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('users:login')
    return render(request, 'users/confirm_logout.html')  # Optional confirmation template


@login_required
def landing_page(request):
    return render(request, 'users/landingpage.html')


@login_required
def profile_view(request):
    """User profile view"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)


@login_required
def settings_view(request):
    """User settings view"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    settings, created = Settings.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'settings': settings,
    }
    return render(request, 'users/settings.html', context)

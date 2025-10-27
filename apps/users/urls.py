from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # User profile and settings
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('settings/', views.settings_view, name='settings'),
]
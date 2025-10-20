from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('artworks/', views.upload_artwork, name='artworks'),
    # path('blogs/', views.create_blog, name='blogs'),
    path('landing/', views.landing_page, name='landing'),
    # path('profile/', views.profile_view, name='profile'),
    # path('settings/', views.settings_view, name='settings'),

    # path('comments/', views.add_comment, name='comments'),
]
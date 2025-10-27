from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('browse/', views.browse, name='browse'),
    path('upload/', views.upload, name='upload'),
    path('artwork/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('artwork/<int:pk>/like/', views.like_artwork, name='like_artwork'),
]
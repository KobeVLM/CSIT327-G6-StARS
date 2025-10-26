from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('badges/', views.badges, name='badges'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
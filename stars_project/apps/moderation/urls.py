from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_dashboard, name='dashboard'),
    path('delete-artwork/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),
    path('dismiss-report/<int:report_id>/', views.dismiss_report, name='dismiss_report'),
    path('suspend-user/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('report-artwork/<int:artwork_id>/', views.report_artwork, name='report_artwork'),
    path('submit-report/', views.submit_report, name='submit_report'),
]
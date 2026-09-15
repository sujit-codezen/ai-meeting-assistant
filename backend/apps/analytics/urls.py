from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('trends/', views.meeting_trends, name='meeting-trends'),
]

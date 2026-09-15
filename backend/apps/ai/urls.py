from django.urls import path
from . import views

urlpatterns = [
    path('qa/', views.meeting_qa, name='meeting-qa'),
    path('search/', views.search_meetings, name='search-meetings'),
]

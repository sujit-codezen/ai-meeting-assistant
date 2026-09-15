from django.db import models
from django.conf import settings


class AnalyticsEvent(models.Model):
    EVENT_TYPES = [
        ('meeting_created', 'Meeting Created'),
        ('meeting_processed', 'Meeting Processed'),
        ('transcription_completed', 'Transcription Completed'),
        ('analysis_completed', 'Analysis Completed'),
        ('task_created', 'Task Created'),
        ('task_completed', 'Task Completed'),
        ('qa_query', 'Q&A Query'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_events'
        ordering = ['-created_at']

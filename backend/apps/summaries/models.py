from django.db import models
from apps.meetings.models import Meeting


class MeetingSummary(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name='summary')
    executive_summary = models.TextField()
    key_points = models.JSONField(default=list)
    sentiment = models.JSONField(default=dict)
    topics = models.JSONField(default=list)
    unresolved_issues = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meeting_summaries'

    def __str__(self):
        return f"Summary for {self.meeting.title}"

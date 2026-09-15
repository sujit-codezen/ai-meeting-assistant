from django.db import models
from apps.meetings.models import Meeting


class Participant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    speaker_label = models.CharField(max_length=50, blank=True)
    mapped_name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'participants'
        unique_together = ['meeting', 'speaker_label']

    def __str__(self):
        return f"{self.name} ({self.speaker_label})"

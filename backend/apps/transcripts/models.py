from django.db import models
from apps.meetings.models import Meeting


class TranscriptSegment(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='segments')
    speaker_label = models.CharField(max_length=50)
    speaker_name = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    start_time = models.FloatField(help_text='Start time in seconds')
    end_time = models.FloatField(help_text='End time in seconds')
    confidence = models.FloatField(default=0.0)
    order = models.IntegerField()

    class Meta:
        db_table = 'transcript_segments'
        ordering = ['start_time']

    def __str__(self):
        return f"[{self.start_time:.1f}s] {self.speaker_label}: {self.text[:50]}"

    @property
    def duration(self):
        return self.end_time - self.start_time

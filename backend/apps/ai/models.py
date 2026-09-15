from django.db import models


class AIProcessingLog(models.Model):
    TASK_TYPES = [
        ('transcription', 'Transcription'),
        ('diarization', 'Diarization'),
        ('summarization', 'Summarization'),
        ('action_extraction', 'Action Extraction'),
        ('decision_extraction', 'Decision Extraction'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('embedding_generation', 'Embedding Generation'),
        ('qa_query', 'Q&A Query'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    meeting_id = models.IntegerField()
    task_type = models.CharField(max_length=30, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    processing_time = models.FloatField(null=True, help_text='Processing time in seconds')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ai_processing_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task_type} - Meeting {self.meeting_id} - {self.status}"

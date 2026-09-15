from django.db import models
from apps.meetings.models import Meeting


class Decision(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='decisions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    context = models.TextField(blank=True, help_text='Original quote from transcript')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'decisions'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

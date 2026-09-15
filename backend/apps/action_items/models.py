from django.db import models
from apps.meetings.models import Meeting
from apps.participants.models import Participant


class ActionItem(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='action_items')
    task = models.TextField()
    assigned_to = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to_name = models.CharField(max_length=100)
    deadline = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    context = models.TextField(blank=True, help_text='Original quote from transcript')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'action_items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task[:50]} - {self.assigned_to_name}"

from rest_framework import serializers
from .models import MeetingSummary


class MeetingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSummary
        fields = ('id', 'meeting', 'executive_summary', 'key_points', 'sentiment', 'topics', 'unresolved_issues', 'created_at')
        read_only_fields = ('id', 'created_at')

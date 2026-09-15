from rest_framework import serializers
from .models import TranscriptSegment


class TranscriptSegmentSerializer(serializers.ModelSerializer):
    duration = serializers.FloatField(read_only=True)

    class Meta:
        model = TranscriptSegment
        fields = ('id', 'speaker_label', 'speaker_name', 'text', 'start_time', 'end_time', 'duration', 'confidence', 'order')

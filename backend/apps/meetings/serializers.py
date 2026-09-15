from rest_framework import serializers
from .models import Meeting
from apps.participants.models import Participant
from apps.transcripts.models import TranscriptSegment
from apps.summaries.models import MeetingSummary
from apps.action_items.models import ActionItem
from apps.decisions.models import Decision


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name', 'email', 'speaker_label', 'mapped_name')


class TranscriptSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptSegment
        fields = ('id', 'speaker_label', 'speaker_name', 'text', 'start_time', 'end_time', 'confidence', 'order')


class MeetingSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSummary
        fields = ('id', 'executive_summary', 'key_points', 'sentiment', 'topics', 'unresolved_issues', 'created_at')


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = ('id', 'task', 'assigned_to_name', 'deadline', 'priority', 'status', 'context', 'created_at')
        read_only_fields = ('id', 'created_at')


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ('id', 'title', 'description', 'reason', 'status', 'context', 'created_at')


class MeetingListSerializer(serializers.ModelSerializer):
    participant_count = serializers.IntegerField(read_only=True)
    action_item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'title', 'description', 'date', 'duration', 'status',
            'file_format', 'file_size', 'participant_count', 'action_item_count',
            'created_at'
        )


class MeetingDetailSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    segments = TranscriptSegmentSerializer(many=True, read_only=True)
    summary = MeetingSummarySerializer(read_only=True)
    action_items = ActionItemSerializer(many=True, read_only=True)
    decisions = DecisionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.__str__', read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'title', 'description', 'date', 'duration', 'recording',
            'file_size', 'file_format', 'status', 'created_by', 'created_by_name',
            'participants', 'segments', 'summary', 'action_items', 'decisions',
            'created_at', 'updated_at'
        )


class MeetingUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'title', 'description', 'date', 'recording')

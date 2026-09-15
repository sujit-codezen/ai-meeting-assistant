from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Meeting
from .serializers import (
    MeetingListSerializer, MeetingDetailSerializer,
    MeetingUploadSerializer
)
from apps.participants.serializers import ParticipantSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at', 'status']

    def get_queryset(self):
        return Meeting.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return MeetingListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return MeetingUploadSerializer
        return MeetingDetailSerializer

    def perform_create(self, serializer):
        meeting = serializer.save(created_by=self.request.user)
        # Set file metadata
        if meeting.recording:
            meeting.file_size = meeting.recording.size
            meeting.file_format = meeting.recording.name.split('.')[-1].upper()
            meeting.save()

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        meeting = self.get_object()
        return Response({
            'id': meeting.id,
            'status': meeting.status,
            'title': meeting.title,
        })

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        meeting = self.get_object()
        if meeting.status != 'uploaded':
            return Response(
                {'error': 'Meeting has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Trigger async processing
        from workers.tasks import transcribe_meeting
        transcribe_meeting.delay(meeting.id)
        meeting.status = 'processing'
        meeting.save()
        return Response({'message': 'Processing started', 'status': meeting.status})

    @action(detail=True, methods=['post'])
    def add_participants(self, request, pk=None):
        meeting = self.get_object()
        serializer = ParticipantSerializer(data=request.data, many=True)
        if serializer.is_valid():
            for participant in serializer.validated_data:
                participant['meeting'] = meeting
                apps_participant = Participant(**participant)
                apps_participant.save()
            return Response(ParticipantSerializer(meeting.participants.all(), many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TranscriptSegment
from .serializers import TranscriptSegmentSerializer


class TranscriptViewSet(viewsets.ModelViewSet):
    serializer_class = TranscriptSegmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TranscriptSegment.objects.filter(meeting__created_by=self.request.user)
        meeting_id = self.request.query_params.get('meeting_id')
        if meeting_id:
            queryset = queryset.filter(meeting_id=meeting_id)
        return queryset

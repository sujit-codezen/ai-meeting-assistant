from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MeetingSummary
from .serializers import MeetingSummarySerializer


class MeetingSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MeetingSummary.objects.filter(meeting__created_by=self.request.user)

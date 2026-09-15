from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Participant
from .serializers import ParticipantSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Participant.objects.filter(meeting__created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Decision
from .serializers import DecisionSerializer


class DecisionViewSet(viewsets.ModelViewSet):
    serializer_class = DecisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Decision.objects.filter(meeting__created_by=self.request.user)
        meeting_id = self.request.query_params.get('meeting_id')
        if meeting_id:
            queryset = queryset.filter(meeting_id=meeting_id)
        return queryset

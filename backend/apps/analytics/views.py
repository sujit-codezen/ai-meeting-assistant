from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import AnalyticsEvent
from .serializers import AnalyticsEventSerializer
from apps.meetings.models import Meeting
from apps.action_items.models import ActionItem
from apps.decisions.models import Decision


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)

    total_meetings = Meeting.objects.filter(created_by=user).count()
    recent_meetings = Meeting.objects.filter(created_by=user, created_at__gte=thirty_days_ago).count()

    total_tasks = ActionItem.objects.filter(meeting__created_by=user).count()
    pending_tasks = ActionItem.objects.filter(meeting__created_by=user, status='pending').count()
    overdue_tasks = ActionItem.objects.filter(
        meeting__created_by=user,
        status='pending',
        deadline__lt=now.strftime('%Y-%m-%d')
    ).count()

    total_decisions = Decision.objects.filter(meeting__created_by=user).count()

    recent_meetings_list = Meeting.objects.filter(created_by=user)[:5]

    return Response({
        'total_meetings': total_meetings,
        'recent_meetings': recent_meetings,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'total_decisions': total_decisions,
        'recent_meetings_list': [
            {
                'id': m.id,
                'title': m.title,
                'date': m.date,
                'status': m.status,
                'duration': str(m.duration) if m.duration else None,
            }
            for m in recent_meetings_list
        ]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meeting_trends(request):
    user = request.user
    days = int(request.query_params.get('days', 30))
    now = timezone.now()

    meetings_by_day = []
    for i in range(days):
        date = now - timedelta(days=i)
        count = Meeting.objects.filter(
            created_by=user,
            created_at__date=date.date()
        ).count()
        meetings_by_day.append({
            'date': date.date().isoformat(),
            'count': count
        })

    return Response({
        'meetings_by_day': list(reversed(meetings_by_day))
    })


class AnalyticsEventViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticsEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnalyticsEvent.objects.filter(user=self.request.user)

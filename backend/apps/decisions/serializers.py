from rest_framework import serializers
from .models import Decision


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ('id', 'meeting', 'title', 'description', 'reason', 'status', 'context', 'created_at')
        read_only_fields = ('id', 'created_at')

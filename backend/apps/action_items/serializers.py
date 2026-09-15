from rest_framework import serializers
from .models import ActionItem


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = (
            'id', 'meeting', 'task', 'assigned_to_name', 'deadline',
            'priority', 'status', 'context', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ActionItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = ('status',)

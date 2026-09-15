from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'file_format', 'created_by', 'created_at')
    list_filter = ('status', 'file_format', 'date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

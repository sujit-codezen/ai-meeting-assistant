from celery import Celery

app = Celery('ai_meeting_workers')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

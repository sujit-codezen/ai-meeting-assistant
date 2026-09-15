import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('ai_meeting')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['workers'])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

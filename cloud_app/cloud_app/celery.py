import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_app.settings')

app = Celery('cloud_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

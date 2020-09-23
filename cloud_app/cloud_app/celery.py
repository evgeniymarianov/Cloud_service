import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_app.settings')

app = Celery('cloud_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'create-report-every-2-minute': {
    'task': 'core.tasks.create_reports_task',
    'schedule': crontab(minute='*/2'),
    },
}

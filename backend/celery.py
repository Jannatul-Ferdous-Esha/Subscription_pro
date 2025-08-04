from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-exchange-rate-hourly': {
        'task': 'core.tasks.fetch_usd_to_bdt_rate',
        'schedule': crontab(minute=0, hour='*'),  # every hour
    },
}
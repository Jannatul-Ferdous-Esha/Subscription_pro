from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask
import json

class Command(BaseCommand):
    help = 'Schedule exchange rate fetch every 3 hours'

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=3,
            period=IntervalSchedule.HOURS,
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Fetch exchange rate every 3 hours',
            task='subscriptions.tasks.fetch_exchange_rate',
        )
        self.stdout.write(self.style.SUCCESS('Scheduled exchange rate fetch task.'))

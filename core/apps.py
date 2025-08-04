from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        if not PeriodicTask.objects.filter(name='Fetch exchange rate every 3 hours').exists():
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=3,
                period=IntervalSchedule.HOURS,
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name='Fetch exchange rate every 3 hours',
                task='core.tasks.fetch_exchange_rate',
            )
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Plan, Subscription, ExchangeRateLog
from django_celery_beat.models import PeriodicTask, IntervalSchedule

admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(ExchangeRateLog)

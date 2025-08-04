from django.db import models
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('cancelled', 'Cancelled'), ('expired', 'Expired')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)




class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=50, null=True, blank=True)
    target_currency = models.CharField(max_length=50,  null=True, blank=True)
    rate = models.FloatField()
    fetched_at = models.DateTimeField()

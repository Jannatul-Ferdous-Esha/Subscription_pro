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

# class ExchangeRateLog(models.Model):
#     base = models.CharField(max_length=10)
#     target = models.CharField(max_length=10)
#     rate = models.FloatField()
#     fetched_at = models.DateTimeField(auto_now_add=True)
# class ExchangeRateView(APIView):
#     def get(self, request):
#         base = request.GET.get('base', 'USD')
#         target = request.GET.get('target', 'BDT')
#         url = f'https://open.er-api.com/v6/latest/{base}'
#         data = requests.get(url).json()
#         rate = data['rates'][target]
        
#         # For each plan, create an ExchangeRateLog entry
#         plans = Plan.objects.all()
#         for plan in plans:
#             ExchangeRateLog.objects.create(
#                 base=str(plan.price),
#                 target=target,
#                 rate=rate,
#             )
        
#         return Response({'rate': rate})
# class ExchangeRateView(APIView):
#     def get(self, request):
#         # Fetch USD to BDT rate
#         url = 'https://open.er-api.com/v6/latest/USD'
#         data = requests.get(url).json()
#         rate = data['rates']['BDT']

#         # Create log for each plan's price
#         plans = Plan.objects.all()
#         for plan in plans:
#             ExchangeRateLog.objects.create(
#                 base='USD',
#                 target='BDT',
#                 rate=rate
#             )

#         return Response({'message': 'Exchange rate logs created for all plans', 'usd_to_bdt_rate': rate})
    
# models.py
# class ExchangeRateLog(models.Model):
#     base = models.CharField(max_length=3, default='USD')  # 'USD'
#     # base_value = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 30.00
#     target = models.CharField(max_length=3, default='BDT')  # 'BDT'
#     rate = models.FloatField()
#     # converted_value = models.FloatField(null=True, blank=True)

#     fetched_at = models.DateTimeField(auto_now_add=True)


class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=50, null=True, blank=True)
    target_currency = models.CharField(max_length=50,  null=True, blank=True)
    rate = models.FloatField()
    # base_amount = models.FloatField()  # <-- new field
    # target_amount = models.FloatField()  # <-- new field
    fetched_at = models.DateTimeField()

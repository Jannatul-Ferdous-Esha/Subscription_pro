from django.shortcuts import render
from datetime import datetime
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .serializers import SubscriptionSerializer
from datetime import date, timedelta
import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from App_Login.forms import PlanForm
from django.shortcuts import redirect
from django.utils import timezone
from .models import Plan, Subscription, ExchangeRateLog
# 4b63e3da9dd67edb1c528abc



def all_subscriptions_view(request):
    users = User.objects.all()
    return render(request, 'subscriptions.html', {'users': users})
def home(request):
    users = User.objects.all()
    return render(request, 'subscriptions.html', {'users': users})

def dashboard_view(request):
    plans = Plan.objects.all()
    exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

    converted_prices = []
    for plan in plans:
        for rate in exchange_rates:
           
            converted_price = float(plan.price) * float(rate.rate)

            converted_prices.append({
                'base': rate.base,
                'target': rate.target,
                'rate': rate.rate,
                'fetched_at': rate.fetched_at,
                'plan_name': plan.name,
                'usd_price': plan.price,
                'converted_price': converted_price,
            })

    subscriptions = Subscription.objects.select_related('user', 'plan').all()

    context = {
        'title': 'Admin Dashboard',
        'plan_form': PlanForm(),
        'plans': plans,
        'subscriptions': subscriptions,
        'exchange_rates': exchange_rates,
        'converted_prices': converted_prices,
    }

    return render(request, 'App_Login/dashboard.html', context)


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Plan, Subscription, ExchangeRateLog
from .serializers import SubscriptionSerializer
from datetime import date, timedelta
import requests
from django.db import connection
from decimal import Decimal
from .serializers import ExchangeRateLogSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)

        start = date.today()
        end = start + timedelta(days=plan.duration_days)
        sub = Subscription.objects.create(user=request.user, plan=plan, start_date=start, end_date=end, status='active')
        return Response({'subscription': SubscriptionSerializer(sub).data}, status=status.HTTP_201_CREATED)

class SubscriptionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user)
        return Response({'subscriptions': SubscriptionSerializer(subs, many=True).data})

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sub_id = request.data.get('subscription_id')
        try:
            sub = Subscription.objects.get(id=sub_id, user=request.user)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

        sub.status = 'cancelled'
        sub.save()
        return Response({'message': 'Subscription cancelled successfully.'})


class ExchangeRateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        
        response = requests.get("https://v6.exchangerate-api.com/v6/4b63e3da9dd67edb1c528abc/latest/USD")
        data = response.json()
        
        if response.status_code != 200 or 'conversion_rates' not in data:
            return Response({"error": "Failed to fetch exchange rate"}, status=500)
        
        rate = data['conversion_rates'].get('BDT')
        if not rate:
            return Response({"error": "BDT rate not found"}, status=500)

        logs = []
        plans = Plan.objects.all()

        for plan in plans:
            base_currency = plan.price  
            target_currency = Decimal(str(rate)) * base_currency

            log = ExchangeRateLog.objects.create(
                base_currency=plan.price ,
                target_currency=Decimal(str(rate)) * base_currency,
                rate=rate,
                fetched_at=datetime.now()
            )
            logs.append({
                "plan_id": plan.id,
                "base_price": base_currency,
                "converted_price": target_currency
            })

        return Response({
            "rate": rate,
            "converted": logs
        })

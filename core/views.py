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

# class SubscribeView(APIView):
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def post(self, request):
#         plan_id = request.data.get('plan_id')
#         plan = Plan.objects.get(id=plan_id)
#         start = date.today()
#         end = start + timedelta(days=plan.duration_days)
#         sub = Subscription.objects.create(user=request.user, plan=plan, start_date=start, end_date=end, status='active')
#         return Response(SubscriptionSerializer(sub).data)

# class SubscriptionListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         subs = Subscription.objects.filter(user=request.user)
#         return Response(SubscriptionSerializer(subs, many=True).data)

# class CancelSubscriptionView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         sub_id = request.data.get('subscription_id')
#         sub = Subscription.objects.get(id=sub_id, user=request.user)
#         sub.status = 'cancelled'
#         sub.save()
#         return Response({'status': 'cancelled'})

# class ExchangeRateView(APIView):
#     def get(self, request):
#         base = request.GET.get('base', 'USD')
#         target = request.GET.get('target', 'BDT')
#         url = f'https://open.er-api.com/v6/latest/{base}'
#         data = requests.get(url).json()
#         rate = data['rates'][target]
#         log = ExchangeRateLog.objects.create(base=base, target=target, rate=rate)
#         return Response({'rate': rate})



def all_subscriptions_view(request):
    users = User.objects.all()
    return render(request, 'subscriptions.html', {'users': users})
def home(request):
    users = User.objects.all()
    return render(request, 'subscriptions.html', {'users': users})
# # def dashboard_view(request):
# #     # plans = Plan.objects.all()
# #     # subscriptions = Subscription.objects.select_related('user', 'plan')
# #     # exchange_rates = ExchangeRateLog.objects.all().order_by('-fetched_at')[:10]  # last 10 rates
# #     # return render(request, 'dashboard.html', {
# #     #     'plans': plans,
# #     #     'subscriptions': subscriptions,
# #     #     'exchange_rates': exchange_rates,
# #     # })
# #     if not request.session.get('admin_username'):
# #         return redirect('App_Login:login')

# #     plans = Plan.objects.all()
# #     subscriptions = Subscription.objects.select_related('user', 'plan')
# #     exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

# #     # Add plan form functionality
# #     plan_form = PlanForm()
# #     if request.method == 'POST':
# #         plan_form = PlanForm(request.POST)
# #         if plan_form.is_valid():
# #             plan_form.save()
# #             return redirect('App_Login:dashboard')

# #     # Enrich exchange rate data with converted plan prices
# #     enriched_rates = []
# #     for rate in exchange_rates:
# #         converted = []
# #         for plan in plans:
# #             converted_price = round(Decimal(plan.price) * Decimal(rate.rate), 2)
# #             converted.append({
# #                 'plan_name': plan.name,
# #                 'usd_price': plan.price,
# #                 'converted_price': converted_price,
# #             })
# #         enriched_rates.append({
# #             'base': rate.base,
# #             'target': rate.target,
# #             'rate': rate.rate,
# #             'fetched_at': rate.fetched_at,
# #             'plans_converted': converted
# #         })

# #     return render(request, 'App_Login/dashboard.html', {
# #         'title': 'Admin Dashboard',
# #         'plans': plans,
# #         'subscriptions': subscriptions,
# #         'exchange_rates': enriched_rates,
# #         'plan_form': plan_form,
# #     })
# # def dashboard_view(request):
# #     if not request.session.get('admin_username'):
# #         return redirect('App_Login:login')

# #     plans = Plan.objects.all()
# #     subscriptions = Subscription.objects.select_related('user', 'plan')
# #     exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

# #     # Add plan form functionality
# #     plan_form = PlanForm()
# #     if request.method == 'POST':
# #         plan_form = PlanForm(request.POST)
# #         if plan_form.is_valid():
# #             plan_form.save()
# #             return redirect('App_Login:dashboard')

# #     # ✅ Get the most recent exchange rate entry
# #     latest_rate = ExchangeRateLog.objects.order_by('-fetched_at').first()
# #     converted_prices = []
# #     for plan in plans:
# #         for rate in exchange_rates:
# #             converted_price = plan.usd_price * rate.rate
# #             converted_prices.append({
# #                 'base': rate.base,
# #                 'target': rate.target,
# #                 'rate': rate.rate,
# #                 'fetched_at': rate.fetched_at,
# #                 'plan_name': plan.plan_name,
# #                 'usd_price': plan.usd_price,
# #                 'converted_price': converted_price,
# #             })
# #     context = {'converted_prices': converted_prices}
# #     return render(request, 'App_Login/dashboard.html', context)
def dashboard_view(request):
    plans = Plan.objects.all()
    exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

    converted_prices = []
    for plan in plans:
        for rate in exchange_rates:
            # Calculate converted price (make sure to convert Decimal & Float to float)
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
# def update_exchange_rate_logs():
#     url = 'https://open.er-api.com/v6/latest/USD'
#     response = requests.get(url)
#     if response.status_code != 200:
#         return

#     data = response.json()
#     rate = data['rates'].get('BDT')
#     if not rate:
#         return

#     fetched_at_str = data.get('time_last_update_utc')
#     fetched_at = datetime.strptime(fetched_at_str, '%a, %d %b %Y %H:%M:%S %z') if fetched_at_str else timezone.now()

#     plans = Plan.objects.all()
#     for plan in plans:
#         ExchangeRateLog.objects.create(
#             base='USD',
#             base_value=plan.price,
#             target='BDT',
#             rate=rate,
#             converted_value=float(plan.price) * rate,
#             fetched_at=fetched_at
#         )

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

# class ExchangeRateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         base = request.GET.get('base', 'USD')
#         target = request.GET.get('target', 'BDT')
#         url = f'https://open.er-api.com/v6/latest/{base}'
#         response = requests.get(url)
#         if response.status_code != 200:
#             return Response({'error': 'Failed to fetch exchange rate.'}, status=500)

#         data = response.json()
#         rate = data['rates'][target]
#         ExchangeRateLog.objects.create(
#             base=base,
#             target=target,
#             rate=rate
#         )
#         return Response({'base': base, 'target': target, 'rate': rate})
# f4d7c37868f6b335d1d22ac963efa1986d15c1f0
# class ExchangeRateView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # base = request.query_params.get('base', 'USD')
#         # target = request.query_params.get('target', 'BDT')

#         url = f"https://v6.exchangerate-api.com/v6/4b63e3da9dd67edb1c528abc/latest/{base}"
#         # 
#         response = requests.get(url)
#         data = response.json()

#         # Handle error if API call fails
#         if response.status_code != 200 or "conversion_rates" not in data:
#             return Response({"error": "Failed to fetch exchange rate"}, status=500)

#         rate = data["conversion_rates"].get("BDT")
#         if rate is None:
#             return Response({"error": "BDT rate not found"}, status=500)

#         logs = []
#         for plan in Plan.objects.all():
#             base = plan.price
#             target = rate * base
#             log = ExchangeRateLog.objects.create(
#                 base="USD",
#                 target="BDT",
#                 rate=rate,
#                 fetched_at=datetime.utcnow(),
#                 base_amount=base,
#                 target_amount=target
#             )
#             logs.append({
#                 "plan_id": plan.id,
#                 "base_amount": base,
#                 "target_amount": target,
#                 "rate": rate,
#                 "fetched_at": log.fetched_at
#             })

#         return Response(logs)
class ExchangeRateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch exchange rate from USD to BDT
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
            base_currency = plan.price  # from Plan table
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
# def test_insert_exchange_rates(request):
#     plans = Plan.objects.all()
#     cursor = connection.cursor()

#     rate = Decimal('117.4567')  # convert float to Decimal

#     for plan in plans:
#         base = plan.price             # likely a Decimal
#         target = (base * rate).quantize(Decimal('0.0001'))  # keep 4 decimal places
#         fetched_at = '2025-08-02 12:00:00'

#         insert_sql = """
#         INSERT INTO core_exchangeratelog (base, target, rate, fetched_at)
#         VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(insert_sql, (base, target, rate, fetched_at))

#     return HttpResponse("Exchange rates inserted.")
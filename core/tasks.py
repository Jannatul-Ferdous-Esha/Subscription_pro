# from celery import shared_task
# import requests
# from .models import ExchangeRateLog

# @shared_task
# def fetch_usd_bdt_rate():
#     url = 'https://open.er-api.com/v6/latest/USD'
#     data = requests.get(url).json()
#     rate = data['rates']['BDT']
#     ExchangeRateLog.objects.create(base_currency='USD', target_currency='BDT', rate=rate)
from celery import shared_task
import requests
from .models import ExchangeRateLog
from .models import Plan, ExchangeRateLog
from decimal import Decimal
from datetime import datetime
@shared_task
def fetch_exchange_rate():
    response = requests.get("https://v6.exchangerate-api.com/v6/4b63e3da9dd67edb1c528abc/latest/USD")
    data = response.json()

    if response.status_code != 200 or 'conversion_rates' not in data:
        return {"error": "Failed to fetch exchange rate"}

    rate = data['conversion_rates'].get('BDT')
    if not rate:
        return {"error": "BDT rate not found"}

    for plan in Plan.objects.all():
        ExchangeRateLog.objects.create(
            base_currency=plan.price,
            target_currency=Decimal(str(rate)) * plan.price,
            rate=rate,
            fetched_at=datetime.now()
        )

    return {"success": True, "rate": rate}
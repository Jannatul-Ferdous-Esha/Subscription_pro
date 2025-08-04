from django.core.management.base import BaseCommand
from core.models import Plan, ExchangeRateLog
from decimal import Decimal
from datetime import datetime
import requests

class Command(BaseCommand):
    help = "Fetches USD to BDT exchange rate and logs converted prices"

    def handle(self, *args, **kwargs):
        response = requests.get("https://v6.exchangerate-api.com/v6/4b63e3da9dd67edb1c528abc/latest/USD")
        data = response.json()

        if response.status_code != 200 or 'conversion_rates' not in data:
            self.stderr.write("Failed to fetch exchange rate")
            return

        rate = data['conversion_rates'].get('BDT')
        if not rate:
            self.stderr.write("BDT rate not found")
            return

        plans = Plan.objects.all()
        for plan in plans:
            base = plan.price
            ExchangeRateLog.objects.create(
                base_currency=base,
                target_currency=Decimal(str(rate)) * base,
                rate=rate,
                fetched_at=datetime.now()
            )
        self.stdout.write("Exchange rates updated.")

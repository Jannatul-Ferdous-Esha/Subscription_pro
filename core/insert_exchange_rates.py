from django.core.management.base import BaseCommand
from core.models import Plan
from django.db import connection

class Command(BaseCommand):
    help = 'Insert exchange rates into core_exchangeratelog using base=Plan.price and target=base*rate'

    def handle(self, *args, **kwargs):
        plans = Plan.objects.all()
        cursor = connection.cursor()

        rate = 117.4567  # Sample rate

        for plan in plans:
            base = plan.price
            target = round(base * rate, 4)
            fetched_at = '2025-08-02 12:00:00'

            insert_sql = """
            INSERT INTO core_exchangeratelog (base, target, rate, fetched_at)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (base, target, rate, fetched_at))

        self.stdout.write(self.style.SUCCESS('Inserted exchange rates into MySQL for all plans.'))

from django.core.management.base import BaseCommand
from order_app.models import Order
from django.utils.timezone import make_aware
from datetime import datetime


class Command(BaseCommand):
    help = 'Update date and time fields from created_at field in Order model'

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(date__isnull=True, time__isnull=True)
        updated_count = 0

        for order in orders:
            order.date = order.created_at.date()
            order.time = order.created_at.time()
            order.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} orders'))

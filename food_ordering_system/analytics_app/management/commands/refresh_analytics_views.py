from django.core.management.base import BaseCommand
from analytics_app.models import DishSalesView, MerchantSalesView, UserActivityView


class Command(BaseCommand):
    help = 'Refreshes all analytics materialized views'

    def handle(self, *args, **options):
        self.stdout.write('Refreshing DishSalesView...')
        DishSalesView.refresh_view()
        self.stdout.write(self.style.SUCCESS('DishSalesView refreshed successfully'))

        self.stdout.write('Refreshing MerchantSalesView...')
        MerchantSalesView.refresh_view()
        self.stdout.write(self.style.SUCCESS('MerchantSalesView refreshed successfully'))

        self.stdout.write('Refreshing UserActivityView...')
        UserActivityView.refresh_view()
        self.stdout.write(self.style.SUCCESS('UserActivityView refreshed successfully'))

        self.stdout.write(self.style.SUCCESS('All analytics views refreshed successfully'))

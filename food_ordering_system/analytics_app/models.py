from django.db import models
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, IntegerField
from django.utils import timezone
from dish_app.models import Dish, Review
from order_app.models import Order, OrderDetail
from user_app.models import User, FavoriteDish

# Create your models here.

class DishSalesView(models.Model):
    """
    Database view for dish sales statistics.
    This is a materialized view that pre-computes sales data for dishes.
    """
    dish = models.OneToOneField(Dish, on_delete=models.DO_NOTHING, primary_key=True)
    total_sales = models.IntegerField()
    online_sales = models.IntegerField()
    offline_sales = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    avg_rating = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'dish_sales_view'

    @classmethod
    def refresh_view(cls):
        """
        Method to refresh the materialized view data.
        This should be called periodically to update the statistics.
        """
        # Clear existing data
        cls.objects.all().delete()

        # Get all dishes
        dishes = Dish.objects.all()

        # Calculate statistics for each dish
        for dish in dishes:
            # Calculate sales
            total_sales = OrderDetail.objects.filter(dish=dish).aggregate(
                total=Sum('quantity'))['total'] or 0

            online_sales = OrderDetail.objects.filter(
                dish=dish,
                order__order_type='online'
            ).aggregate(total=Sum('quantity'))['total'] or 0

            offline_sales = OrderDetail.objects.filter(
                dish=dish,
                order__order_type='offline'
            ).aggregate(total=Sum('quantity'))['total'] or 0

            # Calculate revenue
            total_revenue = OrderDetail.objects.filter(
                dish=dish
            ).aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

            # Calculate average rating
            avg_rating = Review.objects.filter(
                dish=dish
            ).aggregate(avg=Avg('rating'))['avg']

            # Create or update the view record
            cls.objects.create(
                dish=dish,
                total_sales=total_sales,
                online_sales=online_sales,
                offline_sales=offline_sales,
                total_revenue=total_revenue,
                avg_rating=avg_rating
            )


class MerchantSalesView(models.Model):
    """
    Database view for merchant sales statistics.
    This is a materialized view that pre-computes sales data for merchants.
    """
    merchant_id = models.IntegerField(primary_key=True)
    merchant_name = models.CharField(max_length=100)
    total_orders = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    online_orders = models.IntegerField()
    offline_orders = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'merchant_sales_view'

    @classmethod
    def refresh_view(cls):
        """
        Method to refresh the materialized view data.
        This should be called periodically to update the statistics.
        """
        # Clear existing data
        cls.objects.all().delete()

        # Get all merchants with orders
        merchant_orders = Order.objects.values('merchant').annotate(
            merchant_id=F('merchant__id'),
            merchant_name=F('merchant__name'),
            total_orders=Count('id'),
            total_revenue=Sum('total_price'),
            avg_order_value=ExpressionWrapper(
                Sum('total_price') / Count('id'),
                output_field=models.DecimalField(max_digits=10, decimal_places=2)
            ),
            online_orders=Count('id', filter=models.Q(order_type='online')),
            offline_orders=Count('id', filter=models.Q(order_type='offline'))
        )

        # Create view records
        for merchant in merchant_orders:
            cls.objects.create(
                merchant_id=merchant['merchant_id'],
                merchant_name=merchant['merchant_name'],
                total_orders=merchant['total_orders'],
                total_revenue=merchant['total_revenue'],
                avg_order_value=merchant['avg_order_value'],
                online_orders=merchant['online_orders'],
                offline_orders=merchant['offline_orders']
            )


class UserActivityView(models.Model):
    """
    Database view for user activity statistics.
    This is a materialized view that pre-computes user activity data.
    """
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, primary_key=True)
    total_orders = models.IntegerField()
    total_spent = models.DecimalField(max_digits=12, decimal_places=2)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    favorite_dishes_count = models.IntegerField()
    reviews_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_activity_view'

    @classmethod
    def refresh_view(cls):
        """
        Method to refresh the materialized view data.
        This should be called periodically to update the statistics.
        """
        # Clear existing data
        cls.objects.all().delete()

        # Get all users
        users = User.objects.all()

        # Calculate statistics for each user
        for user in users:
            # Calculate order statistics
            orders_data = Order.objects.filter(user=user).aggregate(
                total_orders=Count('id'),
                total_spent=Sum('total_price')
            )

            total_orders = orders_data['total_orders'] or 0
            total_spent = orders_data['total_spent'] or 0

            # Calculate average order value
            avg_order_value = None
            if total_orders > 0:
                avg_order_value = total_spent / total_orders

            # Count favorite dishes
            favorite_dishes_count = FavoriteDish.objects.filter(user=user).count()

            # Count reviews
            reviews_count = Review.objects.filter(user=user).count()

            # Create view record
            cls.objects.create(
                user=user,
                total_orders=total_orders,
                total_spent=total_spent,
                avg_order_value=avg_order_value,
                favorite_dishes_count=favorite_dishes_count,
                reviews_count=reviews_count
            )

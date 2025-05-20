from django.db import models
from user_app.models import User
from merchant_app.models import Merchant
from dish_app.models import Dish


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('completed', 'Completed'),
    ]
    ORDER_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline')
    ]
    ORDER_DINING_STATUS_CHOICES = [
        ('dines_in', 'Dines In'),
        ('reservation', 'Reservation'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, db_index=True)
    order_dining_status = models.CharField(max_length=20, choices=ORDER_DINING_STATUS_CHOICES, default="dines_in", db_index=True)
    date = models.DateField(null=True, blank=True, db_index=True)
    time = models.TimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Add composite indexes for common query patterns
        indexes = [
            # For merchant analytics - merchant + date range queries
            models.Index(fields=['merchant', 'date'], name='merchant_date_idx'),
            # For user order history - user + date range queries
            models.Index(fields=['user', 'date'], name='user_date_idx'),
            # For filtering orders by status and type
            models.Index(fields=['merchant', 'status'], name='merchant_status_idx'),
            # For analytics queries that filter by order type and date
            models.Index(fields=['order_type', 'date'], name='order_type_date_idx'),
            # For queries that filter by multiple criteria
            models.Index(fields=['merchant', 'status', 'order_type'], name='merchant_status_type_idx'),
        ]

    def __str__(self):
        return f'Order by {self.user.full_name} at {self.merchant.name}'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_reviewed = models.BooleanField(default=False, db_index=True)

    class Meta:
        # Add composite indexes for common query patterns
        indexes = [
            # For dish sales analytics
            models.Index(fields=['dish', 'order'], name='dish_order_idx'),
            # For finding unreviewed items
            models.Index(fields=['is_reviewed', 'dish'], name='review_dish_idx'),
            # For joining with order data
            models.Index(fields=['order', 'dish'], name='order_dish_idx'),
        ]

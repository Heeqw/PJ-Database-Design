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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

from rest_framework import serializers
from .models import Order, OrderDetail
from dish_app.models import Dish


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, read_only=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'merchant', 'status', 'order_type', 'total_price', 'created_at', 'updated_at',
                  'details']

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
        fields = ['id', 'user', 'merchant', 'status', 'order_type', 'order_dining_status', 'date', 'time', 'total_price', 'created_at', 'updated_at',
                  'details']

    def create(self, validated_data):
        details_data = validated_data.pop('orderdetail_set')
        order = Order.objects.create(**validated_data)
        for detail_data in details_data:
            OrderDetail.objects.create(order=order, **detail_data)
        return order
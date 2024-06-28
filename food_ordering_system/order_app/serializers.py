from rest_framework import serializers

from common.serializers import ReviewSerializer
from dish_app.models import Review
from dish_app.serializers import DishDetailSerializer
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    dish = DishDetailSerializer()
    review = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'dish', 'quantity', 'price', 'is_reviewed', 'review']

    @staticmethod
    def get_review(obj):
        review = Review.objects.filter(user=obj.order.user, dish=obj.dish).first()
        if review:
            return ReviewSerializer(review).data
        return None


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
from rest_framework import serializers
from .models import User, FavoriteMerchant, FavoriteDish
from order_app.models import Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'gender', 'role', 'student_id', 'staff_id', 'age']


class FavoriteMerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMerchant
        fields = ['id', 'user', 'merchant', 'created_at']


class FavoriteDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteDish
        fields = ['id', 'user', 'dish', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

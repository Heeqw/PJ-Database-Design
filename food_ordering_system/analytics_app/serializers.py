from rest_framework import serializers
from dish_app.models import Dish, Review
from order_app.models import OrderDetail, Order
from user_app.models import User, FavoriteDish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FavoriteDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteDish
        fields = '__all__'

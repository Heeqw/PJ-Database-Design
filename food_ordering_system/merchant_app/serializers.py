from rest_framework import serializers
from .models import Merchant
from dish_app.models import Dish, Review


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MerchantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True, source='dish_set')
    reviews = ReviewSerializer(many=True, read_only=True, source='dish__review_set')

    class Meta:
        model = Merchant
        fields = ['id', 'user', 'name', 'address', 'phone', 'created_at', 'dishes', 'reviews']

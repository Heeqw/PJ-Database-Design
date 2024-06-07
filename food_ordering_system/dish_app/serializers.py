from rest_framework import serializers
from .models import PriceHistory, Dish
from common.serializers import AllergenSerializer, DishSerializer, ReviewSerializer


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'


class DishDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    allergens = AllergenSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'image_url', 'ingredients', 'nutrition_info', 'allergens', 'reviews']
from rest_framework import serializers
from .models import Dish, Review, Allergen


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    dish = DishSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'dish', 'rating', 'comment', 'created_at']

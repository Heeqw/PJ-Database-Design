from rest_framework import serializers
from dish_app.models import Dish, Review, Allergen


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'image_url': {'required': False, 'allow_blank': True},
            'ingredients': {'required': False, 'allow_blank': True},
            'nutrition_info': {'required': False, 'allow_blank': True},
            'allergens': {'required': False}
        }


class DishSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price', 'image_url']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    dish = DishSummarySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'dish', 'rating', 'comment', 'created_at']

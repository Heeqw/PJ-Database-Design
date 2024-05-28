from rest_framework import serializers
from .models import Merchant, MerchantLogin
from dish_app.models import Dish, Review, Allergen
from django.contrib.auth.hashers import make_password


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


class MerchantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'address', 'phone', 'created_at', 'dishes', 'reviews']


class MerchantLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantLogin
        fields = ['merchant', 'username', 'password']
        extra_kwargs = {
            'merchant': {'required': False},
            'password': {'write_only': True},  # 确保密码字段在序列化时是只写的
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # 获取原始密码
        validated_data['password'] = make_password(password)  # 加密密码
        return super().create(validated_data)

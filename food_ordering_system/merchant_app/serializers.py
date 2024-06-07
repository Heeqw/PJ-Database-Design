from rest_framework import serializers
from .models import Merchant, MerchantLogin
from common.serializers import AllergenSerializer, DishSerializer, ReviewSerializer
from django.contrib.auth.hashers import make_password


class MerchantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    featured_dish = DishSerializer(read_only=True)

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'address', 'phone', 'created_at', 'dishes', 'reviews', 'featured_dish']


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

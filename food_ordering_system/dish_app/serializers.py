from rest_framework import serializers
from .models import PriceHistory
from common.serializers import AllergenSerializer, DishSerializer, ReviewSerializer


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'

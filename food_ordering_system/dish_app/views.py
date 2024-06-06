from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from order_app.models import OrderDetail
from user_app.models import FavoriteDish
from .models import Dish, Review, PriceHistory
from .serializers import DishSerializer, ReviewSerializer, AllergenSerializer, PriceHistorySerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum


@api_view(['GET'])
@permission_classes([AllowAny])
def search_dishes(request, merchant_id):
    query = request.GET.get('q')
    if query:
        dishes = Dish.objects.filter(merchant_id=merchant_id, name__icontains=query)
    else:
        dishes = Dish.objects.filter(merchant_id=merchant_id)
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    serializer = DishSerializer(dish)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, dish=dish)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def price_history(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    history = PriceHistory.objects.filter(dish=dish).order_by('-changed_at')
    serializer = PriceHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_favorites_count(request, merchant_id):
    dishes = Dish.objects.filter(merchant_id=merchant_id)
    data = []
    for dish in dishes:
        favorite_count = FavoriteDish.objects.filter(dish=dish).count()
        data.append({
            'dish_id': dish.id,
            'dish_name': dish.name,
            'favorites_count': favorite_count
        })
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_sales_count(request, merchant_id):
    dishes = Dish.objects.filter(merchant_id=merchant_id)
    data = []
    for dish in dishes:
        online_sales = OrderDetail.objects.filter(dish=dish, order__order_type='online').aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
        offline_sales = OrderDetail.objects.filter(dish=dish, order__order_type='offline').aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
        data.append({
            'dish_id': dish.id,
            'dish_name': dish.name,
            'online_sales': online_sales,
            'offline_sales': offline_sales
        })
    return Response(data, status=status.HTTP_200_OK)
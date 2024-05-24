from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Dish, Review
from .serializers import DishSerializer, ReviewSerializer, AllergenSerializer
from django.shortcuts import get_object_or_404


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

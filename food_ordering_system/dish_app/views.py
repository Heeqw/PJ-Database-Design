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
    """
    搜索指定商家的菜品。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数
      - 名称: q
        描述: 搜索关键字
        必需: 否
        类型: 字符串

    响应:
      200:
        描述: 菜品列表
        示例:
          [
            {
              "id": 1,
              "name": "示例菜品",
              "merchant_id": 1,
              "price": 10.99,
              "description": "美味的示例菜品",
              "created_at": "2024-06-07T12:00:00Z",
              "updated_at": "2024-06-07T12:00:00Z"
            }
          ]
    """
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
    """
    获取指定菜品的详细信息。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 菜品详细信息
        示例:
          {
            "id": 1,
            "name": "示例菜品",
            "merchant_id": 1,
            "price": 10.99,
            "description": "美味的示例菜品",
            "created_at": "2024-06-07T12:00:00Z",
            "updated_at": "2024-06-07T12:00:00Z"
          }
    """
    dish = get_object_or_404(Dish, pk=dish_id)
    serializer = DishSerializer(dish)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, dish_id):
    """
    添加对指定菜品的评论。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      201:
        描述: 评论已添加
        示例:
          {
            "id": 1,
            "user": 1,
            "dish": 1,
            "rating": 5,
            "comment": "非常好吃",
            "created_at": "2024-06-07T12:00:00Z"
          }
      400:
        描述: 无效的输入
    """
    dish = get_object_or_404(Dish, pk=dish_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, dish=dish)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def price_history(request, dish_id):
    """
    获取指定菜品的价格历史。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 价格历史
        示例:
          [
            {
              "id": 1,
              "dish": 1,
              "old_price": 9.99,
              "new_price": 10.99,
              "changed_at": "2024-06-07T12:00:00Z"
            }
          ]
    """
    dish = get_object_or_404(Dish, pk=dish_id)
    history = PriceHistory.objects.filter(dish=dish).order_by('-changed_at')
    serializer = PriceHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_favorites_count(request, merchant_id):
    """
    获取指定商家每个菜品的收藏数量。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 菜品收藏数量列表
        示例:
          [
            {
              "dish_id": 1,
              "dish_name": "示例菜品",
              "favorites_count": 100
            }
          ]
    """
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
    """
    获取指定商家每个菜品的销售数量。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 菜品销售数量列表
        示例:
          [
            {
              "dish_id": 1,
              "dish_name": "示例菜品",
              "online_sales": 50,
              "offline_sales": 30
            }
          ]
    """
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
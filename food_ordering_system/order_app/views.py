from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer
from dish_app.models import Dish
from decimal import Decimal
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    """
    下订单。

    参数:
      - 名称: dishes
        描述: 菜品ID列表
        必需: 是
        类型: 数组
        项:
          类型: 整数
      - 名称: merchant
        描述: 商家的ID
        必需: 是
        类型: 整数
      - 名称: order_type
        描述: 订单类型 (在线/离线)
        必需: 是
        类型: 字符串
      - 名称: quantities
        描述: 每个菜品的数量
        必需: 否
        类型: 对象

    响应:
      201:
        描述: 订单已创建
        示例:
          {
            "id": 1,
            "user": 1,
            "merchant": 1,
            "status": "pending",
            "order_type": "online",
            "total_price": 100.99,
            "created_at": "2024-06-07T12:00:00Z",
            "updated_at": "2024-06-07T12:00:00Z"
          }
      400:
        描述: 无效的输入
    """
    dish_ids = request.data.get('dishes', [])
    if not dish_ids:
        return Response({"error": "No dishes provided"}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        user=request.user,
        merchant_id=request.data.get('merchant'),
        status='pending',
        order_type=request.data.get('order_type'),
        total_price=0.0  # Initial price, calculate below
    )

    total_price = Decimal('0.0')
    for dish_id in dish_ids:
        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            continue
        quantity = int(request.data.get('quantities', {}).get(str(dish_id), 1))
        price = Decimal(dish.price) * Decimal(quantity)
        total_price += Decimal(price)
        OrderDetail.objects.create(order=order, dish=dish, quantity=quantity, price=price)

    order.total_price = total_price
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    """
    获取用户的订单历史。

    响应:
      200:
        描述: 订单历史
        示例:
          [
            {
              "id": 1,
              "user": 1,
              "merchant": 1,
              "status": "completed",
              "order_type": "online",
              "total_price": 100.99,
              "created_at": "2024-06-07T12:00:00Z",
              "updated_at": "2024-06-07T12:00:00Z"
            }
          ]
    """
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    print(serializer.data)  # 添加调试打印
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """
    获取指定订单的详细信息。

    参数:
      - 名称: order_id
        描述: 订单的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 订单详细信息
        示例:
          [
            {
              "id": 1,
              "order": 1,
              "dish": 1,
              "quantity": 2,
              "price": 20.99,
              "created_at": "2024-06-07T12:00:00Z",
              "updated_at": "2024-06-07T12:00:00Z"
            }
          ]
      404:
        描述: 订单未找到
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    details = OrderDetail.objects.filter(order=order)
    serializer = OrderDetailSerializer(details, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """
    更新订单状态。

    参数:
      - 名称: order_id
        描述: 订单的ID
        必需: 是
        类型: 整数
      - 名称: status
        描述: 新状态 (preparing/completed)
        必需: 是
        类型: 字符串

    响应:
      200:
        描述: 订单状态已更新
      400:
        描述: 无效的状态
      404:
        描述: 订单未找到
    """
    order = get_object_or_404(Order, id=order_id)
    new_status = request.data.get('status')
    if new_status not in ['preparing', 'completed']:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()
    return Response({'message': 'Order status updated'}, status=status.HTTP_200_OK)
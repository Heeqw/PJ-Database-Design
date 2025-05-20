from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from message_app.models import Notification
from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer
from dish_app.models import Dish
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils.dateparse import parse_date

class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


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
        描述: 订单类型 (online/offline)
        必需: 是
        类型: 字符串
      - 名称: order_dining_status
        描述: 用餐状态 (dines_in/reservation)
        必需: 是
        类型: 字符串
      - 名称: quantities
        描述: 每个菜品的数量
        必需: 否
        类型: 对象
      - 名称: date
        描述: 预订日期（如果是预订）
        必需: 否
        类型: 日期
      - 名称: time
        描述: 预订时间（如果是预订）
        必需: 否
        类型: 时间

    响应:
      201:
        描述: 订单已创建
        示例:
          {
            "id": 1,
            "user": 1,
            "merchant": 1,
            "status": "preparing",
            "order_type": "online",
            "order_dining_status": "dines_in",
            "total_price": 100.99,
            "created_at": "2024-06-07T12:00:00Z",
            "updated_at": "2024-06-07T12:00:00Z",
            "details": [
              {
                "id": 1,
                "order": 1,
                "dish": 1,
                "quantity": 2,
                "price": 20.99
              }
            ]
          }
      400:
        描述: 无效的输入
    """
    dish_ids = request.data.get('dishes', [])
    if not dish_ids:
        return Response({"error": "No dishes provided"}, status=status.HTTP_400_BAD_REQUEST)

    order_type = request.data.get('order_type')
    order_dining_status = request.data.get('order_dining_status')

    try:
        with transaction.atomic():
            now_datetime = now()
            order = Order.objects.create(
                user=request.user,
                merchant_id=request.data.get('merchant'),
                status='preparing',
                order_type=order_type,
                order_dining_status=order_dining_status,
                date=now_datetime.date(),
                time=now_datetime.time(),
                total_price=Decimal('0.0')  # Initial price, calculate below
            )

            total_price = Decimal('0.0')
            for dish_id in dish_ids:
                try:
                    dish = Dish.objects.get(id=dish_id)
                except Dish.DoesNotExist:
                    continue
                quantity = int(request.data.get('quantities', {}).get(str(dish_id), 1))
                price = Decimal(dish.price) * Decimal(quantity)
                total_price += price
                OrderDetail.objects.create(order=order, dish=dish, quantity=quantity, price=price)

            order.total_price = total_price
            order.save()

            # 创建消息通知
            Notification.objects.create(user=request.user, message=f"Your order {order.id} has been placed.")

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    """
    获取用户的订单历史。

    查询参数:
      - status: 订单状态过滤 (preparing/completed)
      - merchant: 商家ID过滤
      - start_date: 开始日期过滤 (YYYY-MM-DD)
      - end_date: 结束日期过滤 (YYYY-MM-DD)
      - order_type: 订单类型过滤 (online/offline)
      - sort: 排序字段 (date/-date/price/-price)
      - page: 页码
      - page_size: 每页数量

    响应:
      200:
        描述: 订单历史
        示例:
          {
            "count": 100,
            "next": "http://api/orders/order_history/?page=2",
            "previous": null,
            "results": [
              {
                "id": 1,
                "user": 1,
                "merchant": 1,
                "status": "completed",
                "order_type": "online",
                "order_dining_status": "dines_in",
                "total_price": 100.99,
                "date": "2024-06-07",
                "time": "12:00:00",
                "created_at": "2024-06-07T12:00:00Z",
                "updated_at": "2024-06-07T12:00:00Z",
                "merchant_name": "示例商家"
              }
            ]
          }
    """
    # 构建过滤条件
    filters = Q(user=request.user)
    
    # 状态过滤
    status = request.query_params.get('status')
    if status:
        filters &= Q(status=status)
    
    # 商家过滤
    merchant_id = request.query_params.get('merchant')
    if merchant_id:
        filters &= Q(merchant_id=merchant_id)
    
    # 日期范围过滤
    start_date = request.query_params.get('start_date')
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            filters &= Q(date__gte=start_date)
    
    end_date = request.query_params.get('end_date')
    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            filters &= Q(date__lte=end_date)
    
    # 订单类型过滤
    order_type = request.query_params.get('order_type')
    if order_type:
        filters &= Q(order_type=order_type)
    
    # 获取订单并应用过滤
    orders = Order.objects.filter(filters)
    
    # 排序
    sort_param = request.query_params.get('sort', '-date')  # 默认按日期降序
    orders = orders.order_by(sort_param)
    
    # 分页
    paginator = OrderPagination()
    paginated_orders = paginator.paginate_queryset(orders, request)
    
    # 序列化
    serializer = OrderSerializer(paginated_orders, many=True)
    
    # 添加商家名称
    for order_data in serializer.data:
        try:
            from merchant_app.models import Merchant
            merchant = Merchant.objects.get(id=order_data['merchant'])
            order_data['merchant_name'] = merchant.name
        except:
            order_data['merchant_name'] = "未知商家"
    
    return paginator.get_paginated_response(serializer.data)


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
          {
            "id": 1,
            "user": 1,
            "merchant": 1,
            "status": "completed",
            "order_type": "online",
            "order_dining_status": "dines_in",
            "total_price": 100.99,
            "created_at": "2024-06-07T12:00:00Z",
            "updated_at": "2024-06-07T12:00:00Z",
            "details": [
              {
                "id": 1,
                "order": 1,
                "dish": 1,
                "quantity": 2,
                "price": 20.99
              }
            ]
          }
      404:
        描述: 订单未找到
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    details = OrderDetail.objects.filter(order=order,quantity__gt=0)
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

    # 创建消息通知
    Notification.objects.create(user=order.user, message=f"Your order {order.id} is now {order.status}.")
    return Response({'message': 'Order status updated'}, status=status.HTTP_200_OK)

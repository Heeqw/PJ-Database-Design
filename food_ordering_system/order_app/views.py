from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer
from dish_app.models import Dish


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
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

    total_price = 0.0
    for dish_id in dish_ids:
        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            continue
        quantity = request.data.get('quantities', {}).get(str(dish_id), 1)
        price = dish.price * quantity
        total_price += price
        OrderDetail.objects.create(order=order, dish=dish, quantity=quantity, price=price)

    order.total_price = total_price
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

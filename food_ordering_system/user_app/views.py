from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, FavoriteDish, FavoriteMerchant
from .serializers import UserSerializer, FavoriteDishSerializer, FavoriteMerchantSerializer, OrderSerializer
from merchant_app.models import Merchant
from order_app.models import Order
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    获取用户个人信息。

    响应:
      200:
        描述: 用户个人信息
        示例:
          {
            "id": 1,
            "username": "示例用户",
            "email": "user@example.com",
            "first_name": "示例",
            "last_name": "用户"
          }
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册。

    响应:
      201:
        描述: 用户已注册
        示例:
          {
            "id": 1,
            "username": "示例用户",
            "email": "user@example.com",
            "first_name": "示例",
            "last_name": "用户"
          }
      400:
        描述: 无效的输入
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    更新用户个人信息。

    响应:
      200:
        描述: 用户个人信息已更新
        示例:
          {
            "id": 1,
            "username": "示例用户",
            "email": "user@example.com",
            "first_name": "示例",
            "last_name": "用户"
          }
      400:
        描述: 无效的输入
    """
    serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    用户登录。

    参数:
      - 名称: username
        描述: 用户名
        必需: 是
        类型: 字符串
      - 名称: password
        描述: 密码
        必需: 是
        类型: 字符串

    响应:
      200:
        描述: 登录成功
        示例:
          {
            "token": "abcdef123456",
            "user": {
              "id": 1,
              "username": "示例用户",
              "email": "user@example.com",
              "first_name": "示例",
              "last_name": "用户"
            }
          }
      401:
        描述: 无效的凭证
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    用户登出。

    响应:
      204:
        描述: 登出成功
    """
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_merchants(request):
    """
    获取用户收藏的商家。

    响应:
      200:
        描述: 用户收藏的商家列表
        示例:
          [
            {
              "id": 1,
              "user": 1,
              "merchant": 1
            }
          ]
    """
    favorites = FavoriteMerchant.objects.filter(user=request.user)
    serializer = FavoriteMerchantSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_dishes(request):
    """
    获取用户收藏的菜品。

    响应:
      200:
        描述: 用户收藏的菜品列表
        示例:
          [
            {
              "id": 1,
              "user": 1,
              "dish": 1
            }
          ]
    """
    favorites = FavoriteDish.objects.filter(user=request.user)
    serializer = FavoriteDishSerializer(favorites, many=True)
    return Response(serializer.data)


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
    return Response(serializer.data)

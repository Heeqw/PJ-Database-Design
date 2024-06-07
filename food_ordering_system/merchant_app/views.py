from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction

from common.serializers import ReviewSerializer, DishSummarySerializer
from merchant_app.models import Merchant, MerchantLogin, MerchantToken
from merchant_app.serializers import MerchantSerializer, MerchantLoginSerializer
from authentication_app.authentication import MerchantTokenAuthentication
from django.contrib.auth.hashers import check_password
from dish_app.models import Dish, PriceHistory, Review
from dish_app.serializers import DishSerializer, PriceHistorySerializer
from order_app.models import Order
from order_app.serializers import OrderSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def search_merchants(request):
    """
    搜索商家。

    参数:
      - 名称: q
        描述: 搜索关键字
        必需: 否
        类型: 字符串

    响应:
      200:
        描述: 商家列表
        示例:
          [
            {
              "id": 1,
              "name": "示例商家",
              "address": "示例地址",
              "phone": "123456789"
              "featured_dish": {
                "id": 1,
                "name": "示例菜品",
                "price": 10.99
              }
            }
          ]
    """
    query = request.GET.get('q')
    if query:
        merchants = Merchant.objects.filter(name__icontains=query)
    else:
        merchants = Merchant.objects.all()
    serializer = MerchantSerializer(merchants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def merchant_detail(request, merchant_id):
    """
    获取商家详细信息。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 商家详细信息
        示例:
          {
            "id": 1,
            "name": "示例商家",
            "address": "示例地址",
            "phone": "123456789"
          }
    """
    merchant = get_object_or_404(Merchant, id=merchant_id)
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_merchant(request):
    """
    创建新商家。

    响应:
      201:
        描述: 商家已创建
        示例:
          {
            "id": 1,
            "name": "示例商家",
            "address": "示例地址",
            "phone": "123456789"
          }
      400:
        描述: 无效的输入
    """
    with transaction.atomic():
        merchant_data = {
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'phone': request.data.get('phone')
        }
        merchant_serializer = MerchantSerializer(data=merchant_data)
        if merchant_serializer.is_valid():
            merchant = merchant_serializer.save()
            if MerchantLogin.objects.filter(username=request.data.get('username')).exists():
                merchant.delete()
                return Response({'username': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
            login_data = {
                'merchant': merchant.id,  # 传递商家ID而不是实例
                'username': request.data.get('username'),
                'password': request.data.get('password') # 使用 make_password 加密密码
            }
            login_serializer = MerchantLoginSerializer(data=login_data)
            if login_serializer.is_valid():
                login_serializer.save()
                return Response(merchant_serializer.data, status=status.HTTP_201_CREATED)
            else:
                merchant.delete()
                return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(merchant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_login(request):
    """
    商家登录。

    参数:
      - 名称: username
        描述: 商家的用户名
        必需: 是
        类型: 字符串
      - 名称: password
        描述: 商家的密码
        必需: 是
        类型: 字符串

    响应:
      200:
        描述: 登录成功
        示例:
          {
            "message": "登录成功",
            "token": "abcdef123456",
            "merchant": {
              "id": 1,
              "name": "示例商家",
              "address": "示例地址",
              "phone": "123456789"
            }
          }
      401:
        描述: 无效的凭证
    """
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        merchant_login_instance = MerchantLogin.objects.get(username=username)
        merchant = merchant_login_instance.merchant
        merchant_data = {
            'id': merchant.id,
            'name': merchant.name,
            'address': merchant.address,
            'phone': merchant.phone
        }
        if check_password(password, merchant_login_instance.password):  # 使用 check_password 验证密码
            token, created = MerchantToken.objects.get_or_create(user=merchant_login_instance)
            return Response({'message': '登录成功', 'token': token.key, 'merchant': merchant_data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    except MerchantLogin.DoesNotExist:
        return Response({'error': '用户名不存在'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def merchant_logout(request):
    """
    商家登出。

    响应:
      204:
        描述: 登出成功
    """
    try:
        request.auth.delete()
    except (AttributeError, MerchantToken.DoesNotExist):
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def manage_merchant(request):
    """
    获取或更新商家信息。

    响应:
      200:
        描述: 商家信息已检索或更新
        示例:
          {
            "id": 1,
            "name": "示例商家",
            "address": "示例地址",
            "phone": "123456789"
          }
      400:
        描述: 无效的输入
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    merchant = merchant_login_instance.merchant
    if request.method == 'POST':
        serializer = MerchantSerializer(merchant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def merchant_info(request):
    """
    获取商家信息。

    响应:
      200:
        描述: 商家信息
        示例:
          {
            "id": 1,
            "name": "示例商家",
            "address": "示例地址",
            "phone": "123456789"
          }
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    merchant = merchant_login_instance.merchant
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def dish_list(request):
    """
    获取商家的菜品列表。

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
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dishes = Dish.objects.filter(merchant=merchant_login_instance.merchant)
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def create_dish(request):
    """
    创建新菜品。

    响应:
      201:
        描述: 菜品已创建
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
      400:
        描述: 无效的输入
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    data = request.data
    data['merchant'] = merchant_login_instance.merchant.id
    serializer = DishSerializer(data=data)
    if serializer.is_valid():
        dish = serializer.save()
        return Response(DishSerializer(dish).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def update_dish(request, dish_id):
    """
    更新菜品信息。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 菜品信息已更新
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
      400:
        描述: 无效的输入
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dish = get_object_or_404(Dish, id=dish_id, merchant=merchant_login_instance.merchant)
    serializer = DishSerializer(dish, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def delete_dish(request, dish_id):
    """
    删除菜品。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      204:
        描述: 菜品已删除
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dish = get_object_or_404(Dish, id=dish_id, merchant=merchant_login_instance.merchant)
    dish.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def update_dish_price(request, dish_id):
    """
    更新菜品价格。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数
      - 名称: new_price
        描述: 新价格
        必需: 是
        类型: 浮点数

    响应:
      200:
        描述: 菜品价格已更新
      400:
        描述: 无效的输入
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dish = get_object_or_404(Dish, id=dish_id, merchant=merchant_login_instance.merchant)
    new_price = request.data.get('new_price')
    if new_price is None:
        return Response({'error': 'New price is required'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        PriceHistory.objects.create(dish=dish, old_price=dish.price, new_price=new_price)
        dish.price = new_price
        dish.save()
    return Response({'message': 'Dish price updated'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def set_featured_dish(request):
    """
    设置主打菜品。

    参数:
      - 名称: dish_id
        描述: 菜品的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 主打菜品已更新
      400:
        描述: 无效的输入
      404:
        描述: 菜品未找到
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    merchant = merchant_login_instance.merchant
    dish_id = request.data.get('dish_id')
    if not dish_id:
        return Response({'error': 'Dish ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        dish = Dish.objects.get(id=dish_id, merchant=merchant)
    except Dish.DoesNotExist:
        return Response({'error': 'Dish does not exist'}, status=status.HTTP_404_NOT_FOUND)

    merchant.featured_dish = dish
    merchant.save()
    return Response({'message': 'Featured dish updated'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def confirm_order(request, order_id):
    """
    确认订单。

    参数:
      - 名称: order_id
        描述: 订单的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 订单状态已更新为完成
      400:
        描述: 无效的状态
      404:
        描述: 订单未找到
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    order = get_object_or_404(Order, id=order_id, merchant=merchant_login_instance.merchant)

    if order.status != 'preparing':
        return Response({'error': 'Only orders that are preparing can be confirmed'},
                        status=status.HTTP_400_BAD_REQUEST)

    order.status = 'completed'
    order.save()
    return Response({'message': 'Order status updated to completed'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def merchant_reviews(request, merchant_id):
    """
    获取指定商户的所有菜品的评价和评分。

    参数:
      - 名称: merchant_id
        描述: 商户的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 商户所有菜品的评价和评分
        示例:
          [
            {
              "id": 1,
              "user": "username",
              "dish": "菜品名称",
              "rating": 5,
              "comment": "很好吃",
              "created_at": "2024-06-07T12:00:00Z"
            }
          ]
    """
    merchant = get_object_or_404(Merchant, id=merchant_id)
    dishes = Dish.objects.filter(merchant=merchant)
    reviews = Review.objects.filter(dish__in=dishes)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_dishes(request, merchant_id):
    """
    在指定商户内搜索菜品。

    参数:
      - 名称: merchant_id
        描述: 商户的ID
        必需: 是
        类型: 整数
      - 名称: q
        描述: 搜索关键字
        必需: 否
        类型: 字符串

    响应:
      200:
        描述: 搜索结果
        示例:
          [
            {
              "id": 1,
              "name": "示例菜品",
              "price": 10.99,
              "image_url": "http://example.com/image.jpg"
            }
          ]
    """
    query = request.GET.get('q')
    if query:
        dishes = Dish.objects.filter(merchant_id=merchant_id, name__icontains=query)
    else:
        dishes = Dish.objects.filter(merchant_id=merchant_id)
    serializer = DishSummarySerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def merchant_orders(request):
    """
    获取商家的订单列表。

    参数:
      - 名称: status
        描述: 订单状态 (可选)
        必需: 否
        类型: 字符串

    响应:
      200:
        描述: 订单列表
        示例:
          [
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
          ]
    """
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    merchant = merchant_login_instance.merchant

    status_filter = request.GET.get('status')
    if status_filter:
        orders = Order.objects.filter(merchant=merchant, status=status_filter)
    else:
        orders = Order.objects.filter(merchant=merchant)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
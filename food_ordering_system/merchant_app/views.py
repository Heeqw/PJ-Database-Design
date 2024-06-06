from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from merchant_app.models import Merchant, MerchantLogin, MerchantToken
from merchant_app.serializers import MerchantSerializer, MerchantLoginSerializer
from authentication_app.authentication import MerchantTokenAuthentication
from django.contrib.auth.hashers import check_password
from dish_app.models import Dish, PriceHistory
from dish_app.serializers import DishSerializer, PriceHistorySerializer
from order_app.models import Order


@api_view(['GET'])
@permission_classes([AllowAny])
def search_merchants(request):
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
    merchant = get_object_or_404(Merchant, id=merchant_id)
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_merchant(request):
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
    try:
        request.auth.delete()
    except (AttributeError, MerchantToken.DoesNotExist):
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def manage_merchant(request):
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
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    merchant = merchant_login_instance.merchant
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def dish_list(request):
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dishes = Dish.objects.filter(merchant=merchant_login_instance.merchant)
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def create_dish(request):
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
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    dish = get_object_or_404(Dish, id=dish_id, merchant=merchant_login_instance.merchant)
    dish.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([MerchantTokenAuthentication])
def update_dish_price(request, dish_id):
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
    token = request.auth
    merchant_login_instance = get_object_or_404(MerchantLogin, auth_token=token)
    order = get_object_or_404(Order, id=order_id, merchant=merchant_login_instance.merchant)

    if order.status != 'preparing':
        return Response({'error': 'Only orders that are preparing can be confirmed'},
                        status=status.HTTP_400_BAD_REQUEST)

    order.status = 'completed'
    order.save()
    return Response({'message': 'Order status updated to completed'}, status=status.HTTP_200_OK)
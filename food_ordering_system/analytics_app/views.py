from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg
from dish_app.models import Dish, Review
from user_app.models import User, FavoriteDish
from order_app.models import Order, OrderDetail
from .serializers import DishSerializer, ReviewSerializer, OrderDetailSerializer, UserSerializer, FavoriteDishSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_statistics(request, merchant_id):
    dishes = Dish.objects.filter(merchant_id=merchant_id)
    data = []
    for dish in dishes:
        reviews = Review.objects.filter(dish=dish)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        total_orders = OrderDetail.objects.filter(dish=dish).count()
        top_customer = OrderDetail.objects.filter(dish=dish).values('order__user').annotate(count=Count('id')).order_by(
            '-count').first()
        data.append({
            'dish': DishSerializer(dish).data,
            'avg_rating': avg_rating,
            'total_orders': total_orders,
            'top_customer': top_customer
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorite_dish(request):
    user_favorites = FavoriteDish.objects.filter(user=request.user)
    data = []
    for favorite in user_favorites:
        sales_online = OrderDetail.objects.filter(dish=favorite.dish, order__order_type='online').count()
        sales_offline = OrderDetail.objects.filter(dish=favorite.dish, order__order_type='offline').count()
        data.append({
            'dish': DishSerializer(favorite.dish).data,
            'sales_online': sales_online,
            'sales_offline': sales_offline
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_loyal_customers(request, merchant_id):
    orders = Order.objects.filter(merchant=merchant_id)
    loyal_customers = orders.values('user').annotate(count=Count('id')).filter(count__gt=5)  # 忠实顾客阈值为5
    data = []
    for customer in loyal_customers:
        user = User.objects.get(pk=customer['user'])
        dishes = OrderDetail.objects.filter(order__user=user, order__merchant_id=merchant_id).values('dish').annotate(
            count=Count('id'))
        data.append({
            'user': UserSerializer(user).data,
            'dishes': dishes
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_activity_analysis(request):
    orders = Order.objects.filter(user=request.user)
    weekly_activity = orders.extra(select={'week': "strftime('%%W', created_at)"}).values('week').annotate(
        count=Count('id')).order_by('week')
    monthly_activity = orders.extra(select={'month': "strftime('%%m', created_at)"}).values('month').annotate(
        count=Count('id')).order_by('month')
    time_activity = orders.extra(select={'hour': "strftime('%%H', created_at)"}).values('hour').annotate(
        count=Count('id')).order_by('hour')
    return Response({
        'weekly_activity': weekly_activity,
        'monthly_activity': monthly_activity,
        'time_activity': time_activity
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_demographics_analysis(request):
    users = User.objects.all()
    role_distribution = users.values('role').annotate(count=Count('id'))
    age_distribution = users.extra(select={'age': "strftime('%Y', 'now') - strftime('%Y', date_of_birth)"}).values(
        'age').annotate(count=Count('id')).order_by('age')
    return Response({
        'role_distribution': role_distribution,
        'age_distribution': age_distribution
    })

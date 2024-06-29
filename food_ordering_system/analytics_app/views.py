from datetime import timedelta
from django.db.models import Count, Avg, Sum, ExpressionWrapper,IntegerField,F
from django.db.models.functions import TruncHour, TruncWeek, TruncMonth, TruncDay
from django.utils import timezone
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dish_app.models import Dish, Review
from order_app.models import Order, OrderDetail
from user_app.models import User, FavoriteDish
from .serializers import DishSerializer, UserSerializer
from collections import defaultdict


# 菜品数据分析
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_statistics(request, merchant_id):
    """
    获取指定商家的菜品统计数据。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 菜品统计数据列表
        示例:
          [
            {
              "dish": {
                "id": 1,
                "name": "示例菜品",
                "merchant_id": 1,
                "price": 10.99,
                "description": "美味的示例菜品",
                "created_at": "2024-06-07T12:00:00Z",
                "updated_at": "2024-06-07T12:00:00Z"
              },
              "avg_rating": 4.5,
              "total_orders": 120,
              "top_customer": {
                "user_id": 1,
                "username": "示例用户",
                "count": 50
              }
            }
          ]
    """
    dishes = Dish.objects.filter(merchant_id=merchant_id)
    data = []
    for dish in dishes:
        reviews = Review.objects.filter(dish=dish)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        total_orders = OrderDetail.objects.filter(dish=dish).count()
        top_customer = OrderDetail.objects.filter(dish=dish).values('order__user').annotate(count=Count('id')).order_by(
            '-count').first()
        if top_customer:
            top_customer_username = User.objects.get(id=top_customer['order__user']).username
            data.append({
                'dish': DishSerializer(dish).data,
                'avg_rating': avg_rating,
                'total_orders': total_orders,
                'top_customer': {
                    'user_id': top_customer['order__user'],
                    'username': top_customer_username,
                    'count': top_customer['count']
                }
            })
        else:
            data.append({
                'dish': DishSerializer(dish).data,
                'avg_rating': avg_rating,
                'total_orders': total_orders,
                'top_customer': None
            })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorite_dish(request):
    """
    获取用户收藏的菜品及其在指定时间范围内的销售数据。

    参数:
      - 名称: period
        描述: 时间范围，可选值为 'week', 'month', 'year'
        必需: 是
        类型: 字符串

    响应:
      200:
        描述: 用户收藏的菜品列表及其销售数据
        示例:
          [
            {
              "dish": {
                "id": 1,
                "name": "示例菜品",
                "merchant_id": 1,
                "price": 10.99,
                "description": "美味的示例菜品",
                "created_at": "2024-06-07T12:00:00Z",
                "updated_at": "2024-06-07T12:00:00Z"
              },
              "sales_online": 50,
              "sales_offline": 30
            }
          ]
    """
    period = request.query_params.get('period')
    if period not in ['week', 'month', 'year']:
        return Response({'error': 'Invalid period. Choose from week, month, year.'}, status=400)

    end_date = now()
    if period == 'week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    elif period == 'year':
        start_date = end_date - timedelta(days=365)
    else:
        return Response({'error': 'Invalid period. Choose from week, month, year.'}, status=400)  # 防止start_date未赋值

    user_favorites = FavoriteDish.objects.filter(user=request.user)
    data = []
    for favorite in user_favorites:
        sales_online = OrderDetail.objects.filter(
            dish=favorite.dish,
            order__order_type='online',
            order__date__range=(start_date, end_date)
        ).count()
        sales_offline = OrderDetail.objects.filter(
            dish=favorite.dish,
            order__order_type='offline',
            order__date__range=(start_date, end_date)
        ).count()
        data.append({
            'dish': DishSerializer(favorite.dish).data,
            'sales_online': sales_online,
            'sales_offline': sales_offline
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_loyal_customers(request, merchant_id):
    """
    获取商家的忠实顾客列表。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 忠实顾客列表
        示例:
          [
            {
              "user": {
                "id": 1,
                "username": "示例用户",
                "email": "user@example.com",
                "first_name": "示例",
                "last_name": "用户"
              },
              "dishes": [
                {
                  "dish": 1,
                  "count": 10
                }
              ]
            }
          ]
    """
    orders = Order.objects.filter(merchant_id=merchant_id)
    loyal_customers = orders.values('user').annotate(count=Count('id')).filter(count__gt=5)  # 忠实顾客阈值为5
    data = []
    for customer in loyal_customers:
        user = User.objects.get(pk=customer['user'])
        dishes = OrderDetail.objects.filter(order__user=user, order__merchant_id=merchant_id).values('dish').annotate(
            count=Count('id'))
        data.append({
            'user': UserSerializer(user).data,
            'dishes': list(dishes)
        })
    return Response(data)


# 用户活跃度分析
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_activity_analysis(request):
    """
    分析用户的活跃度。

    响应:
      200:
        描述: 用户活跃度分析
        示例:
          {
            "weekly_activity": [
              {
                "week": "2024-W01",
                "count": 5
              }
            ],
            "monthly_activity": [
              {
                "month": "2024-01",
                "count": 20
              }
            ],
            "time_activity": [
              {
                "hour": "12",
                "count": 15
              }
            ]
          }
    """
    orders = Order.objects.filter(user=request.user)

    # 手动计算按周统计
    weekly_activity = defaultdict(int)
    for order in orders:
        if order.date:
            week_start = order.date - timedelta(days=order.date.weekday())
            weekly_activity[week_start] += 1

    weekly_activity_list = [{'week': week_start, 'count': count} for week_start, count in sorted(weekly_activity.items())]

    # 手动计算按月统计
    monthly_activity = defaultdict(int)
    for order in orders:
        if order.date:
            month_start = order.date.replace(day=1)
            monthly_activity[month_start] += 1

    monthly_activity_list = [{'month': month_start, 'count': count} for month_start, count in sorted(monthly_activity.items())]

    # 按小时统计
    time_activity = {hour: 0 for hour in range(24)}

    # 统计每小时的订单数
    for order in orders:
        if order.time:
            hour = order.time.hour
            time_activity[hour] += 1

    time_activity_list = [{'hour': hour, 'count': count} for hour, count in sorted(time_activity.items())]

    # 调试输出
    print("Weekly Activity:", weekly_activity_list)
    print("Monthly Activity:", monthly_activity_list)
    print("Time Activity:", time_activity_list)

    return Response({
        'weekly_activity': weekly_activity_list,
        'monthly_activity': monthly_activity_list,
        'time_activity': time_activity_list
    })


# 用户群体特征分析
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_demographics_analysis(request):
    """
    分析用户的群体特征。

    响应:
      200:
        描述: 用户群体特征分析
        示例:
          {
            "role_distribution": [
              {
                "role": "customer",
                "count": 100
              }
            ],
            "age_distribution": [
              {
                "age": "25",
                "count": 50
              }
            ]
          }
    """
    users = User.objects.all()
    role_distribution = users.values('role').annotate(count=Count('id'))

    current_year = timezone.now().year
    age_distribution = users.annotate(
       age=ExpressionWrapper(current_year - F('date_of_birth__year'), output_field=IntegerField())
    ).values('age').annotate(count=Count('id')).order_by('age')
    return Response({
        'role_distribution': list(role_distribution),
        'age_distribution': list(age_distribution)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dish_sales_trend(request, merchant_id):
    """
    获取指定商户的菜品销量趋势分析。

    参数:
      - 名称: merchant_id
        描述: 商家的ID
        必需: 是
        类型: 整数
      - 名称: period
        描述: 时间范围，可选值为 'week', 'month', 'year'
        必需: 是
        类型: 字符串
      - 名称: interval
        描述: 时间间隔，可选值为 'day', 'week', 'month'
        必需: 是
        类型: 字符串

    响应:
      200:
        描述: 菜品销量趋势分析
        示例:
          [
            {
              "dish": {
                "id": 1,
                "name": "示例菜品",
                "merchant_id": 1,
                "price": 10.99,
                "description": "美味的示例菜品",
                "created_at": "2024-06-07T12:00:00Z",
                "updated_at": "2024-06-07T12:00:00Z"
              },
              "sales_trend": [
                {
                  "interval": "2024-01-01",
                  "sales": 30
                },
                {
                  "interval": "2024-01-02",
                  "sales": 25
                }
              ]
            }
          ]
    """
    period = request.query_params.get('period')
    interval = request.query_params.get('interval')
    if period not in ['week', 'month', 'year'] or interval not in ['day', 'week', 'month']:
        return Response({'error': 'Invalid period or interval. Choose from period: week, month, year; interval: day, week, month.'}, status=400)

    end_date = now()
    if period == 'week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    elif period == 'year':
        start_date = end_date - timedelta(days=365)
    else:
        return Response({'error': 'Invalid period. Choose from week, month, year.'}, status=400)  # 防止start_date未赋值

    # 获取商户的所有菜品
    dishes = Dish.objects.filter(merchant_id=merchant_id)
    data = []

    for dish in dishes:
        if interval == 'day':
            sales_trend = OrderDetail.objects.filter(
                dish=dish,
                order__date__range=(start_date, end_date)
            ).annotate(interval=TruncDay('order__date')).values('interval').annotate(sales=Sum('quantity')).order_by('interval')
        elif interval == 'week':
            sales_trend = OrderDetail.objects.filter(
                dish=dish,
                order__date__range=(start_date, end_date)
            ).annotate(interval=TruncWeek('order__date')).values('interval').annotate(sales=Sum('quantity')).order_by('interval')
        elif interval == 'month':
            sales_trend = OrderDetail.objects.filter(
                dish=dish,
                order__date__range=(start_date, end_date)
            ).annotate(interval=TruncMonth('order__date')).values('interval').annotate(sales=Sum('quantity')).order_by('interval')
        else:
            sales_trend = []

        data.append({
            'dish': DishSerializer(dish).data,
            'sales_trend': list(sales_trend)
        })

    return Response(data)
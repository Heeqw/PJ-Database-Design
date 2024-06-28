from django.urls import path
from .views import (dish_statistics, user_favorite_dish, merchant_loyal_customers, user_activity_analysis,
                    user_demographics_analysis, dish_sales_trend)

urlpatterns = [
    path('dish_statistics/<int:merchant_id>/', dish_statistics, name='dish_statistics'),
    path('user_favorite_dish/', user_favorite_dish, name='user_favorite_dish'),
    path('merchant_loyal_customers/<int:merchant_id>/', merchant_loyal_customers, name='merchant_loyal_customers'),
    path('user_activity_analysis/', user_activity_analysis, name='user_activity_analysis'),
    path('user_demographics_analysis/', user_demographics_analysis, name='user_demographics_analysis'),
    path('dish_sales_trend/<int:merchant_id>/', dish_sales_trend, name='dish_sales_trend'),
]

from django.urls import path
from .views import search_dishes, dish_detail, add_review, price_history, dish_favorites_count, dish_sales_count

urlpatterns = [
    path('search/<int:merchant_id>/', search_dishes, name='search_dishes'),
    path('<int:dish_id>/', dish_detail, name='dish_detail'),
    path('<int:dish_id>/add_review/', add_review, name='add_review'),
    path('price_history/<int:dish_id>/',price_history, name='price_history'),
    path('dish_favorites_count/<int:merchant_id>/', dish_favorites_count, name='dish_favorites_count'),
    path('dish_sales_count/<int:merchant_id>/', dish_sales_count, name='dish_sales_count'),
]

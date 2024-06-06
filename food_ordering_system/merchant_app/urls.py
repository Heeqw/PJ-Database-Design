from django.urls import path
from .views import search_merchants, merchant_detail, manage_merchant, merchant_info, create_merchant, merchant_logout, \
    merchant_login, dish_list, create_dish, update_dish, delete_dish, update_dish_price, set_featured_dish, \
    confirm_order

urlpatterns = [
    path('search/', search_merchants, name='search_merchants'),
    path('<int:merchant_id>/', merchant_detail, name='merchant_detail'),
    path('manage/', manage_merchant, name='manage_merchant'),
    path('info/', merchant_info, name='merchant_info'),
    path('create/', create_merchant, name='create_merchant'),
    path('login/', merchant_login, name='merchant_login'),
    path('logout/', merchant_logout, name='merchant_logout'),
    path('dishes/', dish_list, name='dish_list'),
    path('create_dish/', create_dish, name='create_dish'),
    path('update_dish/<int:dish_id>/', update_dish, name='update_dish'),
    path('delete_dish/<int:dish_id>/', delete_dish, name='delete_dish'),
    path('update_dish_price/<int:dish_id>/', update_dish_price, name='update_dish_price'),
    path('set_featured_dish/', set_featured_dish, name='set_featured_dish'),
    path('confirm_order/<int:order_id>/', confirm_order, name='confirm_order'),
]

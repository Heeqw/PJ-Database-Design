from django.urls import path
from .views import profile, register, update_profile, user_login, user_logout, favorite_merchants, favorite_dishes, \
    order_history, add_favorite_merchant, add_favorite_dish

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('profile/update/', update_profile, name='update_profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('favorites/merchants/', favorite_merchants, name='favorite_merchants'),
    path('add_favorite_merchant/', add_favorite_merchant, name='add_favorite_merchant'),
    path('favorites/dishes/', favorite_dishes, name='favorite_dishes'),
    path('add_favorite_dish/', add_favorite_dish, name='add_favorite_dish'),
    path('orders/history/', order_history, name='order_history'),
]

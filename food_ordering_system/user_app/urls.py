from django.urls import path
from .views import profile, register, update_profile, user_logout, favorite_merchants, favorite_dishes, order_history

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('profile/update/', update_profile, name='update_profile'),
    path('logout/', user_logout, name='user_logout'),
    path('favorites/merchants/', favorite_merchants, name='favorite_merchants'),
    path('favorites/dishes/', favorite_dishes, name='favorite_dishes'),
    path('orders/history/', order_history, name='order_history'),
]

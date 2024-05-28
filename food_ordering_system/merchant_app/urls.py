from django.urls import path
from .views import search_merchants, merchant_detail, manage_merchant, merchant_info, create_merchant, merchant_logout, merchant_login

urlpatterns = [
    path('search/', search_merchants, name='search_merchants'),
    path('<int:merchant_id>/', merchant_detail, name='merchant_detail'),
    path('manage/', manage_merchant, name='manage_merchant'),
    path('info/', merchant_info, name='merchant_info'),
    path('create/', create_merchant, name='create_merchant'),
    path('login/', merchant_login, name='merchant_login'),
    path('logout/', merchant_logout, name='merchant_logout'),
]

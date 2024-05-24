from django.urls import path
from .views import search_dishes, dish_detail, add_review

urlpatterns = [
    path('search/<int:merchant_id>/', search_dishes, name='search_dishes'),
    path('<int:dish_id>/', dish_detail, name='dish_detail'),
    path('<int:dish_id>/add_review/', add_review, name='add_review'),
]

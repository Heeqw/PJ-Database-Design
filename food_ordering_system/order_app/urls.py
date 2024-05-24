from django.urls import path
from .views import place_order, order_history

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('order_history/', order_history, name='order_history'),
]

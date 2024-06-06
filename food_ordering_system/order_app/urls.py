from django.urls import path
from .views import place_order, order_history, order_detail, update_order_status

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('order_history/', order_history, name='order_history'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
]

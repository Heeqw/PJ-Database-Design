from django.urls import path
from .views import message_list, mark_as_read

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('messages/<int:pk>/read/', mark_as_read, name='mark-as-read'),
]

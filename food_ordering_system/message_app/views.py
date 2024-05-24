from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list(request):
    messages = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    notification.read = True
    notification.save()
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)

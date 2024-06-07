from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list(request):
    """
    获取用户的消息列表。

    响应:
      200:
        描述: 消息列表
        示例:
          [
            {
              "id": 1,
              "user": 1,
              "message": "示例消息",
              "read": False,
              "created_at": "2024-06-07T12:00:00Z"
            }
          ]
    """
    messages = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, pk):
    """
    将消息标记为已读。

    参数:
      - 名称: pk
        描述: 消息的ID
        必需: 是
        类型: 整数

    响应:
      200:
        描述: 消息已标记为已读
        示例:
          {
            "id": 1,
            "user": 1,
            "message": "示例消息",
            "read": True,
            "created_at": "2024-06-07T12:00:00Z"
          }
      404:
        描述: 消息未找到
    """
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    notification.read = True
    notification.save()
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)

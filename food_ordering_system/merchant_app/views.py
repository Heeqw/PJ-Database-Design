from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Merchant
from .serializers import MerchantSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def search_merchants(request):
    query = request.GET.get('q')
    if query:
        merchants = Merchant.objects.filter(name__icontains=query)
    else:
        merchants = Merchant.objects.all()
    serializer = MerchantSerializer(merchants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def merchant_detail(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_merchant(request):
    merchant = get_object_or_404(Merchant, user=request.user)
    if request.method == 'POST':
        serializer = MerchantSerializer(merchant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_info(request):
    merchant = get_object_or_404(Merchant, user=request.user)
    serializer = MerchantSerializer(merchant)
    return Response(serializer.data)

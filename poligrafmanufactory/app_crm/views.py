from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from app_crm.models import Order
from app_crm.serializers import OrderSerializer


class OrderListApi(ListCreateAPIView):
    """
    List all orders, or create a new order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
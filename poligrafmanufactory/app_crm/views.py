from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from app_crm.models import Order, Counterparty
from app_crm.serializers import OrderSerializer, CounterpartySerializer


class OrderListApi(ListCreateAPIView):
    """
    List all orders, or create a new order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class OrderDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Watch, update or delete order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class CounterpartyListApi(ListCreateAPIView):
    """
    List all counterparties, or crate a new one
    """
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer
    permission_classes = [IsAdminUser]


class CounterpartyDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Watch, update or delete counterparty
    """
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer
    permission_classes = [IsAdminUser]

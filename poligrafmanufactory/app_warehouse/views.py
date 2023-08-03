from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from app_warehouse.models import Shipment
from app_warehouse.serializers import ShipmentSerializer


class ShipmentListApi(ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAdminUser]

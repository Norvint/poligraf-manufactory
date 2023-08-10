import django_filters

from app_warehouse.models import Shipment


class ShipmentFilter(django_filters.FilterSet):
    class Meta:
        model = Shipment
        fields = ['shipped', 'planned_date']

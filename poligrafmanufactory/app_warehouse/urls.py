from django.urls import path, include

from app_warehouse.views import ShipmentListApi

urlpatterns = [
    path('shipments/', include([
        path('', ShipmentListApi.as_view(), name='shipment_list_api')
    ]))
]
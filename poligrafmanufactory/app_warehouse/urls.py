from django.urls import path, include

from app_warehouse.views import ShipmentListApi, ShipmentDetailApi, LoadingListApi, LoadingDetailApi, ShipmentListView

urlpatterns = [
    path('api/', include([
        path('shipments/', include([
            path('', ShipmentListApi.as_view(), name='shipment_list_api'),
            path('<int:pk>', ShipmentDetailApi.as_view(), name='shipment_detail_api'),
        ])),
        path('loadings/', include([
            path('', LoadingListApi.as_view(), name='loading_list_api'),
            path('<int:pk>', LoadingDetailApi.as_view(), name='loading_detail_api')
        ]))
    ])),
    path('shipments/', include([
        path('', ShipmentListView.as_view(), name='shipment_list'),
        # path('<int:pk>', ShipmentDetailApi.as_view(), name='shipment_detail_api'),
    ])),
]

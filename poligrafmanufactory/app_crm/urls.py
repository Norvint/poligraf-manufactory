from django.urls import path, include

from app_crm.views import OrderListApi, CounterpartyListApi, CounterpartyDetailApi, OrderDetailApi

urlpatterns = [
    path('orders/', include([
        path('', OrderListApi.as_view(), name='order_list_api'),
        path('<int:pk>', OrderDetailApi.as_view(), name='order_detail_api'),
    ])),
    path('counterparties/', include([
        path('', CounterpartyListApi.as_view(), name='counterparty_list_api'),
        path('<int:pk>', CounterpartyDetailApi.as_view(), name='counterparty_detail_api'),
    ]))
]

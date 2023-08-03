from django.urls import path, include

from app_crm.views import OrderListApi, CounterpartyListApi

urlpatterns = [
    path('orders/', include([
        path('', OrderListApi.as_view(), name='order_list_api'),
    ])),
    path('counterparties/', include([
        path('', CounterpartyListApi.as_view(), name='counterparty_list_api'),
    ]))
]

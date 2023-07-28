from django.urls import path, include

from app_crm.views import OrderListApi

urlpatterns = [
    path('orders/', include([
        path('', OrderListApi.as_view(), name='order_list_api')
    ]))
]

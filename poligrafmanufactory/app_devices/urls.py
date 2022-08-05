from django.contrib import admin
from django.urls import path

from app_devices.views import InterfaceAdapterListView, DevicesListView

urlpatterns = [
    path('', DevicesListView.as_view(), name='devices_list'),
    path('adapters/', InterfaceAdapterListView.as_view(), name='adapters_list')
]

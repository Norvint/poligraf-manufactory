from django.contrib import admin
from django.urls import path, include

from app_devices.views import InterfaceAdapterListView, DevicesListView, DeviceDetailView, DeviceParametersListView, \
    InterfaceAdapterDetailView, DeviceParametersValuesListView, ReadDeviceParametersView

urlpatterns = [
    path('', include([
        path('', DevicesListView.as_view(), name='devices_list'),
        path('<int:pk>/', include([
            path('',  DeviceDetailView.as_view(), name='device_detail'),
            path('params/', DeviceParametersListView.as_view(), name='device_parameters_list'),
            path('values/', include([
                path('', DeviceParametersValuesListView.as_view(), name='device_parameters_values_list'),
                path('read/', ReadDeviceParametersView.as_view(), name='device_parameters_values_read'),
            ])),
        ])),
    ])),
    path('adapters/', include([
        path('', InterfaceAdapterListView.as_view(), name='adapters_list'),
        path('<int:pk>/', include([
            path('', InterfaceAdapterDetailView.as_view(), name='adapter_detail'),
        ]))
    ]))
]

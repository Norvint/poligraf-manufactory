from django.shortcuts import render
from django.views.generic import ListView

from app_devices.models import InterfaceAdapter, Device
from app_devices.services import check_adapter_availability


class InterfaceAdapterListView(ListView):
    model = InterfaceAdapter
    context_object_name = 'adapters'
    template_name = 'app_devices/adapters_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InterfaceAdapterListView, self).get_context_data(**kwargs)
        for adapter in context['adapters']:
            adapter.status = check_adapter_availability(host=adapter.address, port=adapter.port)
        return context


class DevicesListView(ListView):
    model = Device
    context_object_name = 'devices'
    template_name = 'app_devices/devices_list.html'

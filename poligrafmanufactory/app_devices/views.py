from django.shortcuts import render
from django.views.generic import ListView

from app_devices.models import InterfaceAdapter, Device


class InterfaceAdapterListView(ListView):
    model = InterfaceAdapter
    context_object_name = 'adapters'
    template_name = 'app_devices/adapters_list.html'


class DevicesListView(ListView):
    model = Device
    context_object_name = 'devices'
    template_name = 'app_devices/devices_list.html'

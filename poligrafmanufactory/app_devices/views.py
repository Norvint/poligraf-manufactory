from django.views.generic import ListView, DetailView

from app_devices.models import InterfaceAdapter, Device, DeviceParameter, DeviceParameterValue
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


class InterfaceAdapterDetailView(DetailView):
    model = InterfaceAdapter
    template_name = 'app_devices/adapter_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InterfaceAdapterDetailView, self).get_context_data(**kwargs)
        context['conected_devices'] = Device.objects.filter(interface_adapter=self.get_object())
        return context

class DevicesListView(ListView):
    model = Device
    context_object_name = 'devices'
    template_name = 'app_devices/devices_list.html'


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'app_devices/device_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(DeviceDetailView, self).get_context_data(**kwargs)
    #     # context['device_parameters'] = DeviceParameter.objects.filter(device=self.get_object())
    #     # context['device_parameters_values'] = DeviceParameterValue.objects.filter(parameter__device=self.get_object())
    #     return context


class DeviceParametersListView(DetailView):
    model = Device
    template_name = 'app_devices/device_params_list.html'

    def get_context_data(self, **kwargs):
        context = super(DeviceParametersListView, self).get_context_data(**kwargs)
        context['device_parameters'] = DeviceParameter.objects.filter(device=self.get_object())
        # context['device_parameters_values'] = DeviceParameterValue.objects.filter(parameter__device=self.get_object())
        return context

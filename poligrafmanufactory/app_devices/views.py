import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer

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


class DeviceParametersListView(DetailView):
    model = Device
    template_name = 'app_devices/device_params_list.html'

    def get_context_data(self, **kwargs):
        context = super(DeviceParametersListView, self).get_context_data(**kwargs)
        context['device_parameters'] = DeviceParameter.objects.filter(device=self.get_object())
        return context


class DeviceParametersValuesListView(DetailView):
    model = Device
    template_name = 'app_devices/device_params_values_list.html'

    def get_context_data(self, **kwargs):
        context = super(DeviceParametersValuesListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        device_parameter_values_all = DeviceParameterValue.objects.filter(parameter__device=self.get_object()).order_by('-date', 'parameter__address')
        paginator = Paginator(device_parameter_values_all, 8)
        try:
            device_parameter_values = paginator.page(page)
        except PageNotAnInteger:
            device_parameter_values = paginator.page(1)
        except EmptyPage:
            device_parameter_values = paginator.page(paginator.num_pages)
        context['device_parameters_values'] = device_parameter_values
        return context


class ReadDeviceParametersView(View):

    def get(self, request, *args, **kwargs):
        device = Device.objects.get(pk=kwargs.get('pk'))
        parameters = DeviceParameter.objects.filter(device=device).order_by('title', 'address').distinct('title')
        if parameters:
            client = ModbusTcpClient(
                host=device.interface_adapter.address,
                port=device.interface_adapter.port,
                stopbits=device.interface_adapter.stopbits,
                baudrate=device.interface_adapter.baudrate,
                bytesize=device.interface_adapter.bytesize,
                retries=3,
                framer=ModbusRtuFramer
            )
            for parameter in parameters:
                if parameter.permissions == 'read' or parameter.permissions == 'read/write':
                    quantity_of_registers = DeviceParameter.objects.filter(device=device, title__icontains=parameter.title).count()
                    if 'Holding register' in parameter.parameter_type.title:
                        result = client.read_holding_registers(parameter.address,
                                                               count=quantity_of_registers,
                                                               unit=device.address)
                        for i, param in enumerate(DeviceParameter.objects.filter(device=device, title__icontains=parameter.title).order_by('address')):
                            DeviceParameterValue.objects.create(
                                parameter=param,
                                date=datetime.datetime.now(),
                                value=result.registers[i]
                            )
                    elif 'Coil' in parameter.parameter_type.title:
                        result = client.read_coils(parameter.address,
                                                   count=quantity_of_registers,
                                                   unit=device.address)
                    # print(quantity_of_registers)
            client.close()
            return redirect('device_parameters_values_list', pk=kwargs.get('pk'))
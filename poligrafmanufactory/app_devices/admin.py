from django.contrib import admin

from app_devices.models import InterfaceAdapter, TypeOfDevice, Device, ParameterType, AvailableFunctions, \
    DeviceParameter


@admin.register(InterfaceAdapter)
class InterfaceAdapterAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeOfDevice)
class TypeOfDeviceAdmin(admin.ModelAdmin):
    pass


class DeviceParameterInline(admin.TabularInline):
    model = DeviceParameter
    verbose_name_plural = 'Параметры устройства'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [DeviceParameterInline]


class AvailableFunctionsInline(admin.TabularInline):
    model = AvailableFunctions


@admin.register(ParameterType)
class ParameterTypeAdmin(admin.ModelAdmin):
    inlines = [AvailableFunctionsInline]
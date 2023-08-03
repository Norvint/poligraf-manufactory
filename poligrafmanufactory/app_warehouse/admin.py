from django.contrib import admin

from app_warehouse.models import Shipment, Loading


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Loading)
class LoadingAdmin(admin.ModelAdmin):
    pass

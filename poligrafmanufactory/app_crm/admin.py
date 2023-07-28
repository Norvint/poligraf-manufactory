from django.contrib import admin

from app_crm.models import Counterparty, Order


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_client', 'is_provider']
    search_fields = ['title', 'is_client', 'is_provider']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'date', 'client']
    search_fields = ['number', 'date', 'client']

import logging
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, fields
from rest_framework.validators import UniqueForYearValidator

from app_crm.models import Counterparty, Order
from app_crm.serializers import CounterpartySerializer, OrderSerializer
from app_warehouse.models import Shipment, Loading


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    actual_date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    planned_date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    order = OrderSerializer()

    class Meta:
        model = Shipment
        fields = ['number', 'date', 'name', 'actual_date', 'planned_date', 'shipped', 'order',
                  'order_is_ready']
        validators = [
            UniqueForYearValidator(
                queryset=Shipment.objects.all(),
                field='number',
                date_field='date'
            )
        ]

    def create(self, validated_data):
        raw_order = validated_data.pop('order')
        raw_client = raw_order.pop('client')
        client, client_created = Counterparty.objects.get_or_create(**raw_client)
        order, order_created = Order.objects.get_or_create(**raw_order, client=client)
        shipment = Shipment.objects.create(**validated_data, order=order)
        return shipment

    def update(self, instance, validated_data):
        raw_order = validated_data.pop('order', instance.order)
        if type(raw_order) == OrderedDict:
            try:
                order = Order.objects.get(number=raw_order.get('number'),
                                          date=raw_order.get('date'))
            except ObjectDoesNotExist:
                raw_client = raw_order.pop('client')
                client, client_created = Counterparty.objects.get_or_create(title=raw_client.get('title'))
                order = Order.objects.create(number=raw_order.get('number'),
                                             date=raw_order.get('date'),
                                             client=client)
        else:
            order = raw_order
        instance.order = order
        instance.date = validated_data.get('date', instance.date)
        instance.number = validated_data.get('number', instance.number)
        instance.name = validated_data.get('name', instance.name)
        instance.actual_date = validated_data.get('actual_date', instance.actual_date)
        instance.planned_date = validated_data.get('planned_date', instance.planned_date)
        instance.shipped = validated_data.get('shipped', instance.shipped)
        instance.order_is_ready = validated_data.get('order_is_ready', instance.order_is_ready)
        instance.save()
        return instance


class LoadingSerializer(serializers.HyperlinkedModelSerializer):
    date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    actual_date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    planned_date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    provider = CounterpartySerializer()

    class Meta:
        model = Loading
        fields = ['number', 'date', 'name', 'actual_date', 'planned_date', 'loaded', 'provider']
        validators = [
            UniqueForYearValidator(
                queryset=Loading.objects.all(),
                field='number',
                date_field='date'
            )
        ]

    def create(self, validated_data):
        raw_provider = validated_data.pop('provider')
        provider, provider_created = Counterparty.objects.get_or_create(**raw_provider)
        loading = Loading.objects.create(**validated_data, provider=provider)
        return loading

    def update(self, instance: Loading, validated_data):
        raw_provider = validated_data.pop('provider')
        provider, provider_created = Counterparty.objects.get_or_create(**raw_provider)
        if instance.provider != provider:
            instance.provider = provider
        instance.number = validated_data.get('number', instance.number)
        instance.date = validated_data.get('date', instance.date)
        instance.name = validated_data.get('name', instance.name)
        instance.actual_date = validated_data.get('actual_date', instance.actual_date)
        instance.planned_date = validated_data.get('planned_date', instance.planned_date)
        instance.loaded = validated_data.get('loaded', instance.loaded)
        return instance


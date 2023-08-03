import logging

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
        raw_client = raw_order.pop('client', instance.order.client)
        client, client_created = Counterparty.objects.get_or_create(**raw_client)
        order, order_created = Order.objects.get_or_create(**raw_order, client=client)
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

    class Meta:
        model = Loading
        fields = []

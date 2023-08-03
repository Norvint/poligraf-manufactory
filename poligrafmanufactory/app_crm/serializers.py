from rest_framework import serializers, fields
from rest_framework.validators import UniqueValidator, UniqueForYearValidator

from app_crm.models import Counterparty, Order


class CounterpartySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Counterparty
        fields = ['title', 'is_client', 'is_provider']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    client = CounterpartySerializer()

    class Meta:
        model = Order
        fields = ['number', 'date', 'client']
        validators = [
            UniqueForYearValidator(
                queryset=Order.objects.all(),
                field='number',
                date_field='date'
            )
        ]

    def create(self, validated_data):
        raw_client = validated_data.pop('client')
        client, client_created = Counterparty.objects.get_or_create(**raw_client)
        order = Order.objects.create(**validated_data, client=client)
        return order

    def update(self, instance, validated_data):
        raw_client = validated_data.pop('client')
        client, client_created = Counterparty.objects.get_or_create(
            title=raw_client.get('title', instance.client.title))
        instance.client = client
        instance.date = validated_data.get('date', instance.date)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['client'] = CounterpartySerializer(instance.client, many=False, context={}).data
        return representation

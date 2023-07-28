from rest_framework import serializers, fields

from app_crm.models import Counterparty, Order


class CounterpartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Counterparty
        fields = ['title', 'is_client', 'is_provider']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    date = fields.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'])
    client = fields.CharField()

    class Meta:
        model = Order
        fields = ['number', 'date', 'client']

    def create(self, validated_data):
        client, client_created = Counterparty.objects.get_or_create(title=validated_data.pop('client'))
        order = Order.objects.create(**validated_data, client=client)
        return order

    def update(self, instance, validated_data):
        client, client_created = Counterparty.objects.get_or_create(
            title=validated_data.get('client', instance.client.title))
        instance.client = client
        instance.date = validated_data.get('date', instance.date)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['client'] = CounterpartySerializer(instance.client, many=False, context={}).data
        return representation

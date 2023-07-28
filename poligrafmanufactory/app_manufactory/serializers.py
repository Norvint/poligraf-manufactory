from rest_framework import serializers

from app_manufactory.models import WorkCenter


class WorkCenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkCenter
        fields = ['title']

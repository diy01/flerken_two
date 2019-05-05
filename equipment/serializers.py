from rest_framework import serializers

from equipment.models import *


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

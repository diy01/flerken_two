from rest_framework import serializers

from modules.license.models import *


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'

from rest_framework import serializers
from .models import *


class LicenseSerializer(serializers.ModelSerializer):

    class Meat:
        module = License
        fields = '__all__'

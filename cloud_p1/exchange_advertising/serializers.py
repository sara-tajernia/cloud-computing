from dataclasses import field
from rest_framework import serializers
from .models import *

class advertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertising
        fields = '__all__'



    
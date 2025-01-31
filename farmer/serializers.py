from rest_framework import serializers
from .models import Crop

class CropSerilizers (serializers.ModelSerializer):
    class Meta:
        model=Crop
        fields ='__all__'




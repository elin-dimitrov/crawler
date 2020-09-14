from rest_framework import serializers
from .models import Politic
 

class MinisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politic
        fields = '__all__'
        
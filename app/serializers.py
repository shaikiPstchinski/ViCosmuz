from rest_framework import serializers
from .models import Galaxy, Star, Planet

class GalaxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galaxy
        fields = '__all__'

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = '__all__'

class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = '__all__'

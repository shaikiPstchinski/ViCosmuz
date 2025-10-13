from rest_framework import viewsets
from .models import Galaxy, Star, Planet
from .serializers import GalaxySerializer, StarSerializer, PlanetSerializer 

class GalaxyViewSet(viewsets.ModelViewSet):
    queryset = Galaxy.objects.all()
    serializer_class = GalaxySerializer

class StarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer

class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

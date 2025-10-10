from django.contrib import admin
from .models import Galaxy, Star, Planet

@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'distanceMly')
    
@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'starType', 'galaxy', 'temperature', 'luminosity')

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'star', 'habitable', 'orbitPeriod')
    list_filter = ('habitable', 'star')  
    search_fields = ('name',) 
    list_editable = ('habitable',)
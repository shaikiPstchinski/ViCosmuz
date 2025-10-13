from django.contrib import admin
from .models import CustomUser, Galaxy, Star, Planet

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

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
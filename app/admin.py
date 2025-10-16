from django.contrib import admin
from .models import CustomUser, Galaxy, Star, Planet

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'type', 'is_staff', 'is_active')
    list_filter = ('type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('firstName', 'lastName', 'profilePicture', 'bio')}),
        ('Permissions', {'fields': ('type', 'is_staff', 'is_active', 'groups', 'userPermissions')}),
        ('Important dates', {'fields': ('lastLogin', 'dateJoined')}),
    )

@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'distanceMly')
    
@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'galaxy', 'temperature', 'luminosity')

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'star', 'habitable', 'orbitPeriod')
    list_filter = ('habitable', 'star')  
    search_fields = ('name',) 
    list_editable = ('habitable',)
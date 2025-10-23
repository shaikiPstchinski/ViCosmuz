from django.contrib import admin
from .models import CustomUser, Galaxy, Star, Planet

@admin.action(description='Mark selected users as verified')
def markAsVerified(self, request, queryset):
    queryset.update(verified=True)
    self.message_user(request, f'{request} user(s) marked as verified.')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    actions = ['markAsVerified']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profilePicture', 'bio')}),
        ('Type and Verification', {'fields': ('type', 'verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'verified', 'is_staff', 'is_active'),
        }),
    )

    def verifiedStatus(self, obj):
        return "✅" if obj.verified else "❌"
    verifiedStatus.short_description = 'Verified'
    verifiedStatus.admin_order_field = "verified"

@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'distanceMly')
    
@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'galaxy', 'temperature', 'luminosity')

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'star', 'habitable', 'orbitPeriod')
    list_filter = ('habitable', 'star')  
    search_fields = ('name',) 
    list_editable = ('habitable',)
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps

def createUserRoles(sender, **kwargs):
    if sender.name == 'ViCosmus':
        user_group, _ =  Group.objects.get_or_create(name='User')
        astronomer_group, _ = Group.objects.get_or_create(name='Astronomer')
        administrator_group, _ = Group.objects.get_or_create(name='Administrator')

        galaxy_permissions = Permission.objects.filter(content_type__app_label='ViCosmus', content_type__model='galaxy')
        star_permissions = Permission.objects.filter(content_type__app_label='ViCosmus', content_type__model='star')
        planet_permissions = Permission.objects.filter(content_type__app_label='ViCosmus', content_type__model='planet')

        for permission in list(galaxy_permissions) + list(star_permissions) + list(planet_permissions):
            if permission.startswith('add_', 'change_ ', 'delete_ '):
                astronomer_group.permissions.add(permission)

        for permission in Permission.objects.all():
            administrator_group.permissions.add(permission)
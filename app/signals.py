from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps

def createUserRoles(sender, **kwargs):
    if sender.name == 'ViCosmuz':
        userGroup, _ =  Group.objects.get_or_create(name='User')
        astronomerGroup, _ = Group.objects.get_or_create(name='Astronomer')
        administratorGroup, _ = Group.objects.get_or_create(name='Administrator')

        galaxyPermissions = Permission.objects.filter(content_type__app_label='ViCosmuz', content_type__model='galaxy')
        starPermissions = Permission.objects.filter(content_type__app_label='ViCosmuz', content_type__model='star')
        planetPermissions = Permission.objects.filter(content_type__app_label='ViCosmuz', content_type__model='planet')

        for permission in list(galaxyPermissions) + list(starPermissions) + list(planetPermissions):
            if permission.codename.startswith('add_', 'change_ ', 'delete_ ', 'view_'):
                astronomerGroup.permissions.add(permission)

        for permission in list(galaxyPermissions) + list(starPermissions) + list(planetPermissions):
            if permission.objects.filter(codename__startswith='view_'):
                userGroup.permissions.add(permission)

        for permission in Permission.objects.all():
            administratorGroup.permissions.add(permission)
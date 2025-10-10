from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=60, choices=[('user', 'User'), ('astronomer', 'Astronomer'), ('admin', 'Administrator')], verbose_name="User's role", default='user')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField('auth.Group', blank=True, help_text="User's group", related_name="userGroup", related_query_name='user', verbose_name='groups')

    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name="userGroup", verbose_name="user's permissions")

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'custom_user'

class CelestialBody(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Celestial body's name")
    mass = models.FloatField(verbose_name="Body's mass", null=True, blank=True)
    radius = models.FloatField(verbose_name="Body's radius", null=True, blank=True)
    description = models.TextField(verbose_name="Celestial body's description", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Galaxy(CelestialBody):
    type = models.CharField(max_length=255, verbose_name="Galaxy's type")
    distanceMly = models.FloatField(verbose_name='Distance in millions light-years')

class Star(CelestialBody):
    galaxy = models.ForeignKey(Galaxy, on_delete=models.CASCADE, related_name='stars')
    starType = models.CharField(max_length=255, verbose_name="Star's type")
    temperature = models.FloatField(null=True, blank=True, verbose_name="Star's surface temperature")
    luminosity = models.FloatField(null=True, blank=True, verbose_name="Star's luminosity")

    
class Planet(CelestialBody):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="Planets")
    habitable = models.BooleanField(default=False, verbose_name="Planet has or hasn't habitable conditions")
    orbitPeriod = models.FloatField(null=True, blank=True, verbose_name="Orbital period in Earth years")



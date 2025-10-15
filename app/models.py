from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    TYPE_CHOICES = [
        ('user', 'User'),
        ('astronomer', 'Astronomer'),
        ('admin', 'Administrator'),
    ]

    type = models.CharField(max_length=60, choices=TYPE_CHOICES, verbose_name="User's role", default='user', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Profile picture")
    bio = models.TextField(blank=True, verbose_name="User's biography")
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} {self.email}'
    
    class Meta:
        db_table = 'custom_user'  

class CelestialBody(models.Model):
    TYPES = [
        ('galaxy', 'Galaxy'),
        ('star', 'Star'),
        ('planet', 'Planet'),
        ('moon', 'Moon'),
        ('asteroid', 'Asteroid'),
        ('comet', 'Comet'),
        ('black_hole', 'Black Hole'),
        ('nebula', 'Nebula'),
        ('cluster', 'Cluster'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255, unique=True, verbose_name="Celestial body's name")
    type = models.CharField(max_length=255, choices=TYPES, verbose_name="Celestial body's type")
    mass = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Body's mass", null=True, blank=True)
    radius = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="Body's radius", null=True, blank=True)
    description = models.TextField(verbose_name="Celestial body's description", blank=True)
    discoveryDate = models.DateField(null=True, blank=True, verbose_name="Discovery date")
    discoveredBy = models.CharField(max_length=255, blank=True, verbose_name="Discover's name")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False, verbose_name="Data verified by an astronomer")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Celestial Bodies"
        ordering = ['-discoveryDate']
        abstract = True

class Galaxy(CelestialBody):
    type = models.CharField(max_length=255, verbose_name="Galaxy's type", choices=[('spiral', 'Spiral'), ('elliptical', 'Elliptical'), ('irregular', 'Irregular')])
    distanceMly = models.FloatField(verbose_name='Distance in millions light-years')
    image = models.ImageField(upload_to='galaxyImages/', null=True, blank=True, verbose_name="Galaxy's image")

class Star(CelestialBody):
    Content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    galaxy = GenericForeignKey('Content_type', 'object_id')
    starType = models.CharField(max_length=255, verbose_name="Star's type", choices=[('main_sequence', 'Main Sequence'), ('giant', 'Giant'), ('dwarf', 'Dwarf'), ('supergiant', 'Supergiant')])
    temperature = models.FloatField(null=True, blank=True, verbose_name="Star's surface temperature")
    luminosity = models.FloatField(null=True, blank=True, verbose_name="Star's luminosity")
    image = models.ImageField(upload_to='starImages/', null=True, blank=True, verbose_name="Star's image")
    
class Planet(CelestialBody):
    name = models.CharField(max_length=255, unique=True, verbose_name="Planet's name")
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="planets")
    habitable = models.BooleanField(default=False, verbose_name="Planet has habitable conditions")
    orbitPeriod = models.FloatField(null=True, blank=True, verbose_name="Orbital period in earth years")
    image = models.ImageField(upload_to='planetImages/', null=True, blank=True, verbose_name="Planet's image")



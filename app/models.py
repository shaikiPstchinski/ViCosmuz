from django.db import models

class Galaxy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Galaxy's name")
    type = models.CharField(max_length=255, verbose_name="Galaxy's type")
    distance_mly = models.FloatField(verbose_name='Distance in millions light-years')

    def __str__(self):
        return self.name
    
class Star(models.Model):
    name = models.CharField(max_length=255, verbose_name="Star's name")
    galaxy = models.ForeignKey(Galaxy, on_delete=models.CASCADE, related_name='Stars')
    starType = models.CharField(max_length=255, verbose_name="Star's type")
    magnitude = models.FloatField(verbose_name="Star's magnitude value")

    def __str__(self):
        return self.name
    
class Planet(models.Model):
    name = models.CharField(max_length=255)
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name="Planets")
    has_life = models.BooleanField(default=False, verbose_name="Planet has or hasn't life")
    orbit_period = models.FloatField(verbose_name="Orbit period in Earth years")

    def __str__(self):
        return self.name


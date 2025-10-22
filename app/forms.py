from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CelestialBodyForm(forms.ModelForm):
    CHOICES = [
        ('star', 'Star'),
        ('planet', 'Planet'),
        ('moon', 'Moon'),
        ('asteroid', 'Asteroid'),
        ('comet', 'Comet'),
    ]
    widgets = { 'description': forms.Textarea(attrs={'rows':3})   }
    name = forms.CharField(max_length=255, label='Name')
    type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(choices=CHOICES), label='Body Type')
    mass = forms.FloatField(label='Mass')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    discoveryDate = forms.DateField(label='Discovery Date', widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), input_formats=['%Y-%m-%d', '%d/%m/%Y'])
    discoveredBy = forms.CharField(max_length=255, label='Discovered By')
    image = forms.ImageField(label='Image', required=False)

    class Meta:
        model = CelestialBody
        fields = '__all__'

        labels = {
            'name': 'Name',
            'bodyType': 'Body Type',
            'mass': 'Mass',
            'description': 'Description',
            'discoveryDate': 'Discovery Date',
            'discoveredBy': 'Discovered By',
            'image': 'Image',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),  
        }

class GalaxyForm(CelestialBodyForm):
    class Meta:
        model = Galaxy
        fields = '__all__'
        exclude = ['type']

class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = '__all__'
        exclude = ['content_type', 'object_id', 'type']

class PlanetForm(CelestialBodyForm):
    class Meta:
        model = Planet
        fields = '__all__'
        exclude = ['type']

class CelestialBodyTypeForm(CelestialBodyForm):
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
    objectType = forms.ChoiceField(choices=TYPES, label='Celestial Body Type')
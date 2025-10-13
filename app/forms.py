from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CelestialBody, Galaxy, Star, Planet

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CelestialBodyForm(forms.ModelForm):
    class Meta:
        model = CelestialBody
        fields = '__all__'

        widgets = {
            'discoveryDate': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),  
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class GalaxyForm(forms.ModelForm):
    class Meta:
        model = Galaxy
        fields = '__all__'

class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = '__all__'

class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = '__all__'
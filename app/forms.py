from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CelestialBody

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'type')

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
        fields = ('username', 'email', 'profile_picture', 'bio', 'type')
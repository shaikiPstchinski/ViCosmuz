from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet

def galaxy_list(request):
    galaxies = Galaxy.objects.all()
    return render(request, 'galaxyList.html', {'galaxies':galaxies})

def search(request):
    query = request.GET.get('q', '')
    galaxies = Galaxy.objects.filter(name__icontains=query)
    stars = Star.objects.filter(name__icontains=query)
    planets = Planet.objects.filter(name__icontains=query)
    context = {'query':query, 'galaxies':galaxies, 'stars':stars, 'planets':planets}

    return render(request, 'search.html', context)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)

            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('login')
        
    else: 
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form':form})


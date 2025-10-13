from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CelestialBodyForm, GalaxyForm, StarForm, PlanetForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet
from django.contrib.auth.decorators import login_required, user_passes_test

def is_astronomer(user):
    return user.groups.authenticated and user.user_type == 'astronomer'

@login_required
@user_passes_test(is_astronomer)
def addCelestialBody(request):
    if request.method == 'POST':
        form = CelestialBodyForm(request.POST, request.FILES)
        if form.is_valid():
            celestialBody = form.save(commit=False)
            celestialBody.discoveredBy = request.user.username
            celestialBody.save()
            messages.success(request, f'Celestial body: {celestialBody.name} added successfully.')
            return redirect('home')
    else:
        return render(request, 'add_celestial_body.html', {'form': form})

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

def galaxy_detail(request, galaxy_id):
    galaxy = get_object_or_404(Galaxy, id=galaxy_id)
    stars = galaxy.stars.all()

    return render(request, 'galaxyDetail.html', {'galaxy': galaxy, 'stars': stars})

def star_detail(request, star_id):
    star = get_object_or_404(Star, id=star_id)
    planets = star.planets.all()

    return render(request, 'starDetail.html', {'star': star, 'planets': planets})

def planet_detail(request, planet_id):
    planet = get_object_or_404(Planet, id=planet_id)

    return render(request, 'planetDetail.html', {'planet': planet})

def create_galaxy(request):
    if request.method == 'POST':
        form = GalaxyForm(request.POST, request.FILES)
        if form.is_valid():
            galaxy = form.save()
            messages.success(request, f'Galaxy {galaxy.name} created successfully.')
            return redirect('home')
    else:
        form = GalaxyForm()

    return render(request, 'createGalaxy.html', {'form': form})

def create_star(request):
    if request.method == 'POST':
        form = StarForm(request.POST, request.FILES)
        if form.is_valid():
            star = form.save()
            messages.success(request, f'Star {star.name} created successfully.')
            return redirect('home')
    else:
        form = StarForm()

    return render(request, 'createStar.html', {'form': form})

def create_planet(request):
    if request.method == 'POST':
        form = PlanetForm(request.POST, request.FILES)
        if form.is_valid():
            planet = form.save()
            messages.success(request, f'Planet {planet.name} created successfully.')
            return redirect('home')
    else:
        form = PlanetForm()

    return render(request, 'createPlanet.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import astronomer_required

def isAstronomer(user):
    return user.groups.authenticated and user.user_type == 'astronomer'

def galaxyList(request):
    galaxies = Galaxy.objects.all()
    return render(request, 'galaxyList.html', {'galaxies':galaxies})

def search(request):
    query = request.GET.get('q', '')
    selectedType = request.GET.get('type', '')
    galaxies = [] 
    stars = [] 
    planets = [] 

    results = False
    
    if query and not selectedType:
        galaxies = Galaxy.objects.filter(name__icontains=query)
        stars = Star.objects.filter(name__icontains=query)
        planets = Planet.objects.filter(name__icontains=query)
        results = True
        context = {'query': query, 'galaxies': galaxies, 'stars': stars, 'planets': planets}
        return render(request, 'search.html', context)

    return render(request, 'search.html', context)

    if selectedType:
        results = True

        if selectedType == 'galaxy':
            galaxies = Galaxy.objects.all()
            
            name = request.GET.get('name', '')
            if name:
                galaxies = galaxies.filter(name__icontains=name)
            
            galaxy_type = request.GET.get('galaxy_type', '')
            if type:
                galaxies = galaxies.filter(type=galaxy_type)
            
            distanceMly = request.GET.get('distance_mly', '')
            if distanceMly:
                try:
                    galaxies = galaxies.filter(distanceMly__lte=float(distance_mly))
                except ValueError:
                    pass
        
        elif selected_type == 'star':
            stars = Star.objects.all()
            
            name = request.GET.get('name', '')
            if name:
                stars = stars.filter(name__icontains=name)
            
            starType = request.GET.get('starType', '')
            if starType:
                stars = stars.filter(type=starType)
            
            temperature = request.GET.get('temperature', '')
            if temperature:
                try:
                    stars = stars.filter(temperature__lte=float(temperature))
                except ValueError:
                    pass
            
            luminosity = request.GET.get('luminosity', '')
            if luminosity:
                try:
                    stars = stars.filter(luminosity__lte=float(luminosity))
                except ValueError:
                    pass
        
        elif selectedType == 'planet':
            planets = Planet.objects.all()
            
            name = request.GET.get('name', '')
            if name:
                planets = planets.filter(name__icontains=name)
            
            star = request.GET.get('star', '')
            if star:
                planets = planets.filter(star__name__icontains=star)

            habitable = request.GET.get('habitable', '')
            if habitable == 'yes':
                planets = planets.filter(habitable=True)
            elif habitable == 'no':
                planets = planets.filter(habitable=False)
            
            orbitPeriod = request.GET.get('orbitPeriod', '')
            if orbitPeriod:
                try:
                    planets = planets.filter(orbitalPeriod__lte=float(orbitalPeriod))
                except ValueError:
                    pass

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

def galaxyDetail(request, galaxy_id):
    galaxy = get_object_or_404(Galaxy, id=galaxy_id)
    stars = galaxy.stars.all()

    return render(request, 'galaxyDetail.html', {'galaxy': galaxy, 'stars': stars})

def starDetail(request, star_id):
    star = get_object_or_404(Star, id=star_id)
    planets = star.planets.all()

    return render(request, 'starDetail.html', {'star': star, 'planets': planets})

def planetDetail(request, planet_id):
    planet = get_object_or_404(Planet, id=planet_id)

    return render(request, 'planetDetail.html', {'planet': planet})

#@login_required
#@user_passes_test(isAstronomer)
def celestialBodyCreation(request):
    title = "Criar Corpo Celeste"
    selectedType = request.POST.get('type') or request.GET.get('type')
    form = None

    if request.method == 'POST':
        selectedType = request.POST.get('objectType')

        if selectedType == 'galaxy':
            form = GalaxyForm(request.POST, request.FILES)
            title = "Criar Galáxia"
        elif selectedType == 'star':
            form = StarForm(request.POST, request.FILES)
            title = "Criar Estrela"
        elif selectedType == 'planet':
            form = PlanetForm(request.POST, request.FILES)
            title = "Criar Planeta"
        else: form = None

        if form and form.is_valid():
            celestialBody = form.save(commit=False)
            celestialBody.discoveredBy = request.user.username
            celestialBody.save()
            messages.success(request, f'Corpo celeste criado com sucesso: {celestialBody.name}.')
            return redirect('home')
        else:
            context = {'form': form, 'title': title, 'selectedType': selectedType}
            return render(request, 'celestialBodyCreation.html', context)

    else:
        if not selectedType:
            form = CelestialBodyTypeForm()
        if selectedType == 'galaxy':
            form = GalaxyForm()
            title = "Criar Galáxia"
        elif selectedType == 'star':
            form = StarForm()
            title = "Criar Estrela"
        elif selectedType == 'planet':
            form = PlanetForm()
            title = "Criar Planeta"
        else: 
            form = CelestialBodyTypeForm()
        
        context = {'form': form, 'title': title, 'selectedType': selectedType}
        return render(request, 'celestialBodyCreation.html', context)

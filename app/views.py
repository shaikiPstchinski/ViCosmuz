from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import astronomerRequired
import random
import requests

def randomGalaxy():
    ids = list(Galaxy.objects.values_list('id', flat=True))

    if not ids:
        return redirect('galaxies')
 
    while randomId not in ids:
        randomId = random.randint(1, 9)

    return render(requests, 'GalaxyDetail.html', {'galaxy': get_object_or_404(Galaxy, id=randomId)})

def randomStar():
    ids = list(Galaxy.objects.values_list('id', flat=True))

    if not ids:
        return redirect('stars')
 
    while randomId not in ids:
        randomId = random.randint(1, 9)

    return render(requests, 'StarDetail.html', {'star': get_object_or_404(Star, id=randomId)})

def randomPlanet():
    ids = list(Planet.objects.values_list('id', flat=True))

    if not ids:
        return redirect('planets')

    randomId = random.randint(1, 9)
    return redirect('starDetail', star_id=randomId)

def isAstronomer(user):
    pass

def random_galaxy(request):
    ids = list(Galaxy.objects.values_list('id', flat=True))
    if not ids:
        return redirect('galaxies')  
    random_id = random.choice(ids)
    return redirect('galaxy_detail', pk=random_id)

def random_star(requests):
    ids = list(Star.objects.values_list('id', flat=True))
    if not ids:
        return redirect('stars')
    random_id = random.choice(ids)
    return redirect('star_detail', pk=random_id)

def random_planet(requests):
    ids = list(Planet.objects.values_list('id', flat=True))
    if not ids:
        return redirect('planets')
    random_id = random.choice(ids)
    return redirect('planet_detail', pk=random_id)

def galaxyList(requests):
    galaxies = Galaxy.objects.all()
    return render(requestss, 'galaxyList.html', {'galaxies':galaxies})

def search(requests):
    query = requests.GET.get('q', '')
    selectedType = requests.GET.get('type', '')
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
        return render(requests, 'search.html', context)

    return render(requests, 'search.html', context)

    if selectedType:
        results = True

        if selectedType == 'galaxy':
            galaxies = Galaxy.objects.all()
            
            name = request.GET.get('name', '')
            if name:
                galaxies = galaxies.filter(name__icontains=name)
            
            galaxyType = requests.GET.get('type', '')
            if objectType:
                galaxies = galaxies.filter(type=galaxy_type)

            
            distanceMly = requests.GET.get('distance_mly', '')
            if distanceMly:
                try:
                    galaxies = galaxies.filter(distanceMly__lte=float(distance_mly))
                except ValueError:
                    pass
        
        elif selectedType == 'star':
            stars = Star.objects.all()
            
            name = requests.GET.get('name', '')
            if name:
                stars = stars.filter(name__icontains=name)
            
            starType = requests.GET.get('type', '')
            if starType:
                stars = stars.filter(type=starType)
            
            temperature = requests.GET.get('temperature', '')
            if temperature:
                try:
                    stars = stars.filter(temperature__lte=float(temperature))
                except ValueError:
                    pass
            
            luminosity = requests.GET.get('luminosity', '')
            if luminosity:
                try:
                    stars = stars.filter(luminosity__lte=float(luminosity))
                except ValueError:
                    pass
        
        elif selectedType == 'planet':
            planets = Planet.objects.all()
            
            name = requests.GET.get('name', '')
            if name:
                planets = planets.filter(name__icontains=name)
            
            star = requests.GET.get('star', '')
            if star:
                planets = planets.filter(star__name__icontains=star)

            habitable = requests.GET.get('habitable', '')
            if habitable == 'yes':
                planets = planets.filter(habitable=True)
            elif habitable == 'no':
                planets = planets.filter(habitable=False)
            
            orbitPeriod = requests.GET.get('orbitPeriod', '')
            if orbitPeriod:
                try:
                    planets = planets.filter(orbitalPeriod__lte=float(orbitalPeriod))
                except ValueError:
                    pass

def home(requests):
    return render(requests, 'home.html')

def register(requests):
    if requests.method == 'POST':
        form = CustomUserCreationForm(requests.POST)
        if form.is_valid():
            user = form.save()

            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)

            messages.success(requests, 'Usuário cadastrado com sucesso.')
            return redirect('login')
        
    else: 
        form = CustomUserCreationForm()

    return render(requests, 'register.html', {'form':form})

def galaxyDetail(requests, galaxy_id):
    galaxy = get_object_or_404(Galaxy, id=galaxy_id)
    stars = galaxy.stars.all()

    return render(requests, 'galaxyDetail.html', {'galaxy': galaxy, 'stars': stars})

def starDetail(requests, star_id):
    star = get_object_or_404(Star, id=star_id)
    planets = star.planets.all()

    return render(requests, 'starDetail.html', {'star': star, 'planets': planets})

def planetDetail(requests, planet_id):
    planet = get_object_or_404(Planet, id=planet_id)

    return render(requests, 'planetDetail.html', {'planet': planet})

@astronomerRequired
def celestialBodyCreation(requests):
    title = "Criar Corpo Celeste"
    objectType = requests.POST.get('objectType') if requests.method == 'POST' else None 
    galaxyForm = GalaxyForm(requests.POST or None, requests.FILES or None)
    starForm = StarForm(requests.POST or None, requests.FILES or None)
    planetForm = PlanetForm(requests.POST or None, requests.FILES or None)

    if requests.method == 'POST': 
        form = None
        
        match(objectType):
            case 'galaxy':
                form = galaxyForm
            case 'star':
                form = starForm
            case 'planet':
                form = planetForm

        if form and form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(requests, f"{selectedType.capitalize()} '{obj.name}' criada com sucesso!")
        else:
            messages.error(requests, "Erro ao criar o corpo celeste. Verifique os campos e tente novamente.")
            print(form.errors if form else "❌ Nenhum formulário selecionado.")
            
        selectedType = requests.POST.get("objectType") if requests.method == "POST" else None

    return render(requests, "celestialBodyCreation.html", {
        "title": title,
        "galaxyForm": galaxyForm,
        "starForm": starForm,
        "planetForm": planetForm,
        "selectedType": selectedType,
    })

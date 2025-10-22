from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import astronomerRequired
import random

def randomGalaxy():
    ids = list(Galaxy.objects.values_list('id', flat=True))

    if not ids:
        return redirect('galaxies')
 
    while randomId not in ids:
        randomId = random.randint(1, 9)

    return render(request, 'GalaxyDetail.html', {'galaxy': get_object_or_404(Galaxy, id=randomId)})

def randomStar():
    ids = list(Galaxy.objects.values_list('id', flat=True))

    if not ids:
        return redirect('stars')
 
    while randomId not in ids:
        randomId = random.randint(1, 9)

    return render(request, 'StarDetail.html', {'star': get_object_or_404(Star, id=randomId)})

def randomPlanet():
    ids = list(Planet.objects.values_list('id', flat=True))

    if not ids:
        return redirect('planets')

    randomId = random.randint(1, 9)
    return redirect('starDetail', star_id=randomId)

def isAstronomer(user):
def random_galaxy(request):
    ids = list(Galaxy.objects.values_list('id', flat=True))
    if not ids:
        return redirect('galaxies')  
    random_id = random.choice(ids)
    return redirect('galaxy_detail', pk=random_id)

def random_star(request):
    ids = list(Star.objects.values_list('id', flat=True))
    if not ids:
        return redirect('stars')
    random_id = random.choice(ids)
    return redirect('star_detail', pk=random_id)

def random_planet(request):
    ids = list(Planet.objects.values_list('id', flat=True))
    if not ids:
        return redirect('planets')
    random_id = random.choice(ids)
    return redirect('planet_detail', pk=random_id)


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
            
            galaxyType = request.GET.get('type', '')
            if objectType:
                galaxies = galaxies.filter(type=galaxy_type)

            
            distanceMly = request.GET.get('distance_mly', '')
            if distanceMly:
                try:
                    galaxies = galaxies.filter(distanceMly__lte=float(distance_mly))
                except ValueError:
                    pass
        
        elif selectedType == 'star':
            stars = Star.objects.all()
            
            name = request.GET.get('name', '')
            if name:
                stars = stars.filter(name__icontains=name)
            
            starType = request.GET.get('type', '')
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

@astronomerRequired
def celestialBodyCreation(request):
    title = "Criar Corpo Celeste"
    objectType = None 
    galaxyForm = GalaxyForm()
    starForm = StarForm()
    planetForm = PlanetForm()

    if request.method == 'POST':
        objectType = request.POST.get('objectType')

        if objectType == "galaxy":
            title = "Criar Galáxia"
            galaxyForm = GalaxyForm(request.POST, request.FILES)

            if galaxyForm.is_valid():
                galaxy = galaxyForm.save(commit=False)
                galaxy.discoveredBy = request.user.username
                galaxy.save()
                if galaxyForm.is_valid():
                    galaxy = galaxyForm.save(commit=False)
                    galaxy.discoveredBy = request.user.username
                    galaxy.save()
                    print(f"[✅ DATABASE] Galaxy '{galaxy.name}' saved successfully!")

                messages.success(request, f'Galáxia criada com sucesso: {galaxy.name}.')
                return redirect('home')
            else:
                print("Form error:\n", galaxyForm.errors)
                print("[❌ INVALID GALAXY FORM]")

        elif objectType == "star":
            title = "Criar Estrela"
            starForm = StarForm(request.POST, request.FILES)

            if starForm.is_valid():
                star = starForm.save(commit=False)
                star.discoveredBy = request.user.username
                star.save()
                messages.success(request, f'Estrela criada com sucesso: {star.name}.')
                return redirect('home')
            else:
                print("Form error:\n", starForm.errors)

        elif objectType == "planet":
            title = "Criar Planeta"
            planetForm = PlanetForm(request.POST, request.FILES)

            if planetForm.is_valid():
                planet = planetForm.save(commit=False)
                planet.discoveredBy = request.user.username
                planet.save()
                messages.success(request, f'Planeta criado com sucesso: {planet.name}.')
                return redirect('home')
            else:
                print("Form error:\n", planetForm.errors)
        else:
            messages.error(request, 'Tipo de corpo celeste inválido.')
            print("Object type error:\n", objectType)

    print("=== Celestial Body Creation Debug ===")
    print("Request method:", request.method)
    print("POST content:", request.POST)
    print("Selected type:", objectType)
    print("Galaxy form valid:", galaxyForm.is_valid())
    print("Star form valid:", starForm.is_valid())
    print("Planet form valid:", planetForm.is_valid())

    context = {
        'title': title,
        'objectType': objectType,
        'galaxyForm': galaxyForm,
        'starForm': starForm,
        'planetForm': planetForm,
        }

    return render(request, 'celestialBodyCreation.html', context)

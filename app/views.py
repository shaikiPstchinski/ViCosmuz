from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Galaxy, Star, Planet
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import astronomerRequired

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
    selectedType = None

    galaxyForm = GalaxyForm()
    starForm = StarForm()
    planetForm = PlanetForm()

    if request.method == 'POST':
        selectedType = request.POST.get('objectType')
        if selectedType == "galaxy":
            title = "Criar Galáxia"
            galaxyForm = GalaxyForm(request.POST, request.FILES)

            if galaxyForm.is_valid():
                galaxy = galaxyForm.save(commit=False)
                galaxy.discoveredBy = request.user.username
                galaxy.save()
                messages.success(request, f'Galáxia criada com sucesso: {galaxy.name}.')
                return redirect('home')

        elif selectedType == "star":
            title = "Criar Estrela"
            starForm = StarForm(request.POST, request.FILES)

            if starForm.is_valid():
                star = starForm.save(commit=False)
                star.discoveredBy = request.user.username
                star.save()
                messages.success(request, f'Estrela criada com sucesso: {star.name}.')
                return redirect('home')

        elif selectedType == "planet":
            title = "Criar Planeta"
            planetForm = PlanetForm(request.POST, request.FILES)

            if planetForm.is_valid():
                planet = planetForm.save(commit=False)
                planet.discoveredBy = request.user.username
                planet.save()
                messages.success(request, f'Planeta criado com sucesso: {planet.name}.')
                return redirect('home')
        else:
            form = None
            messages.error(request, "Tipo de corpo celeste inválido.")

    print("I'm here")
    print("Request method:", request.method)
    print("POST content:", request.POST)
    print("Selected type:", selectedType)
    print("Galaxy form valid?", galaxyForm.is_valid())
    print("Star form valid?", starForm.is_valid())
    print("Planet form valid?", planetForm.is_valid())

    context = {
        'title': title,
        'selectedType': selectedType,
        'galaxyForm': galaxyForm,
        'starForm': starForm,
        'planetForm': planetForm,
        }

    return render(request, 'celestialBodyCreation.html', context)

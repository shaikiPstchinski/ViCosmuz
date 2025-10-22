from django.urls import include, path
from django.contrib.auth import logout, views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('galaxy/<int:galaxyId>/', views.galaxyDetail, name='galaxyDetail'),
    path('celestialBodyCreation/', views.celestialBodyCreation, name='celestialBodyCreation'),
    path('star/<int:starId>/', views.starDetail, name='starDetail'),
    path('planet/<int:planetId>/', views.planetDetail, name='planetDetail'),
    path('create/', views.celestialBodyCreation, name='createCelestialBody'),
]


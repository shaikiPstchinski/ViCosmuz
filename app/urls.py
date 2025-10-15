from django.urls import include, path
from django.contrib.auth import logout, views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('galaxy/<int:galaxy_id>/', views.galaxyDetail, name='galaxyDetail'),
    path('celestialBodyCreation/', views.celestialBodyCreation, name='celestialBodyCreation'),
    path('star/<int:star_id>/', views.starDetail, name='starDetail'),
    path('planet/<int:planet_id>/', views.planetDetail, name='planetDetail'),
    path('create/', views.celestialBodyCreation, name='createCelesrtialBody'),
    path('', include('ViCosmuz.urls')),
    path('api/', include('app.urls_api')),
]


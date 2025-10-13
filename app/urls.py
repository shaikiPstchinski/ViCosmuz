from django.urls import include, path
from django.contrib.auth import logout, views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('galaxy/<int:galaxy_id>/', views.galaxy_detail, name='galaxyDetail'),
    path('star/<int:star_id>/', views.star_detail, name='starDetail'),
    path('planet/<int:planet_id>/', views.planet_detail, name='planetDetail'),
    path('add/galaxy/', views.create_galaxy, name='createGalaxy'),
    path('', include('ViCosmuz.urls')),
    path('api/', include('app.urls_api')),
]


from django.urls import include, path
from django.contrib.auth import logout, views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('galaxies/', views.galaxy_list, name='galaxyList'),
    path('', include('ViCosmuz.urls')),
]


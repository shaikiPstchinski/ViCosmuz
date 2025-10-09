from django.urls import path
from django.contrib.auth import logout, views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='app/templates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('search/', views.search, name='search'),
    path('galaxies/', views.galaxy_list, name='galaxyList'),
]


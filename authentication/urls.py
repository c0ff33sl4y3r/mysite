from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('register', views.register, name = "register"),
    path('login', views.loginn, name = "login"),
    path('logout', views.logoutt, name = "logout"),
    path('profile', views.profile, name = "profile"),
    path('pacman',views.pacman, name="pacman")
]

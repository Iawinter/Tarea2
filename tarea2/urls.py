"""tarea2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from futbol import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('leagues', views.LigasList.as_view()),
    path('teams', views.EquiposList.as_view()),
    path('players', views.JugadoresList.as_view()),
    path('leagues/<str:id>', views.LigasUnico.as_view()),
    path('teams/<str:id>', views.EquiposUnico.as_view()),
    path('players/<str:id>', views.JugadoresUnico.as_view()),
    path('leagues/<str:id>/teams', views.EquiposLiga.as_view()),
    path('leagues/<str:id>/players', views.JugadoresLiga.as_view()),
    path('teams/<str:id>/players', views.JugadoresEquipo.as_view()),
    path('teams/<str:id>/players/train', views.EquipoTrain.as_view()),
    path('leagues/<str:id>/teams/train', views.LigaTrain.as_view()),
    path('players/<str:id>/train', views.JugadorTrain.as_view()),
]

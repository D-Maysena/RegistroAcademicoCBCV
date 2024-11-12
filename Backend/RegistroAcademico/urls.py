from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',  views.login, name="login"),
    path('inicio/',  views.inicio, name="inicio"),
    path('notas/',  views.registrarNotas, name="notas"),
    
    #RUTAS API
    path('cargarEstudiantes/',  views.cargarEstudiantes, name="cargarEstudiantes"),
    path('cargarAsignaturas/',  views.cargarAsignaturas, name="cargarAsignaturas"),
    path('cargarNotas/',  views.cargarNotas, name="cargarNotas"),
]

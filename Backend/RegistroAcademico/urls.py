from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',  views.login, name="login"),
    path('inicio/',  views.inicio, name="inicio"),
    path('notas/',  views.registrarNotas, name="notas"),
    path('estudiantes/',  views.estudiantes, name="estudiantes"),
    #Agregar uno nuevo
    path('agregarEstudiante/',  views.agregarEstudiante, name="agregarEstudiante"),
    #Editar info
    path('agregarEstudianteEditar/<str:codestudiante>',  views.agregarEstudiante, name="agregarEstudianteEditar"),

    path('infoEstudiante/<str:codestudiante>',  views.infoEstudiante, name="infoEstudiante"),
    path('eliminarEstudiante/<str:codestudiante>',  views.eliminarEstudiante
         , name="eliminarEstudiante"),
    
    
    #RUTAS API
    path('estudiante/',  views.EstudiantesAPI, name="Estudiantes"),
    path('cargarEstudiantes/',  views.cargarEstudiantes, name="cargarEstudiantes"),
    path('cargarAsignaturas/',  views.cargarAsignaturas, name="cargarAsignaturas"),
    path('cargarNotas/',  views.cargarNotas, name="cargarNotas"),
]

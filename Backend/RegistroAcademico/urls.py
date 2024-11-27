from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',  views.loginView, name="login"),
    path('inicio/',  views.inicio, name="inicio"),
    path('notas/',  views.registrarNotas, name="notas"),
    path('estudiantes/',  views.estudiantes, name="estudiantes"),
    #Agregar uno nuevo
    path('agregarEstudiante/',  views.agregarEstudiante, name="agregarEstudiante"),
    path('agregarEstudianteT/<str:tutor_id>',  views.agregarEstudiante, name="agregarEstudianteT"),
    
    path('agregar2/',  views.agregar2, name="agregar2"),
    #Editar info
    path('agregarEstudianteEditar/<str:codestudiante>',  views.agregarEstudiante, name="agregarEstudianteEditar"),

    path('infoEstudiante/<str:codestudiante>',  views.infoEstudiante, name="infoEstudiante"),
    path('eliminarEstudiante/<str:codestudiante>',  views.eliminarEstudiante, name="eliminarEstudiante"),
    
    #Inscripcion
    path('inscripcionAsignatura/',  views.inscribirAsignaturas, name="inscripcionAsignatura"),
    path('inscripcionAula/',  views.inscribirAula, name="inscripcionAula"),
    
    path('consultarNotas/',  views.consultarNotas, name="consultarNotas"),
    
    
    
    path('asignarDocente/',  views.asignarDocente, name="asignarDocente"),
    
    path('horarios/',  views.horarios, name="horarios"),
    
    
    
    path('gestionDocentes/',  views.gestionDocentes, name="gestionDocentes"),
    path('agregarDocente/',  views.agregarDocente, name="agregarDocente"),
    path('agregarDocenteEditar/<str:ceduladocente>',  views.agregarDocente, name="agregarDocenteEditar"),
    path('infoDocente/<str:ceduladocente>',  views.infoDocente, name="infoDocente"),
    path('eliminarDocente/<str:ceduladocente>',  views.eliminarDocente, name="eliminarDocente"),
    
    path('agregar2/<str:estudiantegregado>/', views.agregar2, name='agregar2'),
    path('agregarTutor/', views.agregarTutor, name='agregarTutor'),
    
    
    #RUTAS API
    path('docente/',  views.DocentesAPI, name="docente"),
    path('consultarNotasAPI/',  views.consultarNotasAPI, name="consultarNotasAPI"),
    path('estudiante/',  views.EstudiantesAPI, name="Estudiantes"),
    path('asignatura/',  views.AsignaturasAPI, name="Asignaturas"),
    path('cargarEstudiantes/',  views.cargarEstudiantes, name="cargarEstudiantes"),
    path('cargarAsignaturas/',  views.cargarAsignaturas, name="cargarAsignaturas"),
    path('cargarNotas/',  views.cargarNotas, name="cargarNotas"),
]

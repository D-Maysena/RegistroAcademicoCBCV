from django.contrib import admin
from . models import Asignacionaula,Asignatura, Asignaciondocente,Aula,Docente,Estudiante,Grupo,Horario,Inscribe,Registronotas,Turno,Tutor
# Register your models here.
admin.site.register(Asignacionaula)
admin.site.register(Asignaciondocente)
admin.site.register(Asignatura)
admin.site.register(Aula)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Grupo)
admin.site.register(Horario)
admin.site.register(Inscribe)
admin.site.register(Registronotas)
admin.site.register(Turno)
admin.site.register(Tutor)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from .forms import SeleccionGrupoAsignatura
from .models import Estudiante, Inscribe, Registronotas, Asignatura
from django.http import JsonResponse
from datetime import datetime

def login(request):
  if request.method =="POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user  = authenticate(request,username=username, password=password)
    if user is None:
      messages.error(request, "No se encuentra al usuario")
      return render(request, "./login.html")
    else:
      messages.success(request, "Inicio de sesión exitoso")
      return redirect("inicio")
  else:   
    return render(request, "./login.html")
  
def inicio(request):
  return render(request, "./inicio.html")

def registrarNotas(request):
    form = SeleccionGrupoAsignatura()
    print("form")
    
    if request.method == "POST":
        form1 = SeleccionGrupoAsignatura(request.POST)
        if form1.is_valid(): 
            asignatura = form1.cleaned_data['Asignatura']
            estudiante = form1.cleaned_data['estudiante']
            
            # Obtener los valores de los parciales y nota final, y manejarlos si están vacíos
            parcial1 = request.POST.get('parcial1', '').strip()  # Usamos '' como valor por defecto
            parcial2 = request.POST.get('parcial2', '').strip()
            parcial3 = request.POST.get('parcial3', '').strip()
            parcial4 = request.POST.get('parcial4', '').strip()
            notafinal = request.POST.get('notafinal', '').strip()

            # Convertir a int solo si no están vacíos
            if parcial1:
                parcial1 = float(parcial1)
            else:
                parcial1 = None

            if parcial2:
                parcial2 = float(parcial2)
            else:
                parcial2 = None

            if parcial3:
                parcial3 = float(parcial3)
            else:
                parcial3 = None

            if parcial4:
                parcial4 = float(parcial4)
            else:
                parcial4 = None

            if notafinal:
                notafinal = float(notafinal)
            else:
                notafinal = None

            print(parcial1, parcial2, parcial3, parcial4, notafinal)
            
            año_actual = datetime.now().year

            try:
                print("update")
                print(asignatura)
                print(estudiante)
                # Solo actualizamos los campos que no estén vacíos
                defaults = {}

                if parcial1 is not None:
                    defaults['parcial1'] = parcial1
                if parcial2 is not None:
                    defaults['parcial2'] = parcial2
                if parcial3 is not None:
                    defaults['parcial3'] = parcial3
                if parcial4 is not None:
                    defaults['parcial4'] = parcial4
                if notafinal is not None:
                    defaults['notafinal'] = notafinal

                if defaults:

                    busqueda = Registronotas.objects.get(codestudiante=estudiante, codigoasignatura=asignatura)
                    print("busqueda")
                    print(busqueda)
                    # Intenta actualizar o crear el registro utilizando `update_or_create`
                    registro, creado = Registronotas.objects.update_or_create(
                        codestudiante=busqueda.codestudiante,
                        codigoasignatura=busqueda.codigoasignatura,
                        periodoacademico=año_actual,
                        defaults=defaults
                    )
                    print("registro")
                    print(registro)
                    if creado:
                        print("El registro no existía y se ha creado uno nuevo.")
                    else:
                        print("El registro existía y ha sido actualizado.")
        
                print("Operación completada exitosamente")
            except Exception as e:
                print(f"Error: {e}")
        
        return render(request, "./notas.html", {
            "form": form
        })
    
    else:
        return render(request, "./notas.html", {
            "form": form
        })

def cargarEstudiantes(request):
  grupo_id = request.GET.get('grupo', '').strip()
  if not grupo_id:
    estudiantes_grupo = Estudiante.objects.all()
  else:
    estudiantes_grupo =Estudiante.objects.filter(codigogrupo=grupo_id)
   
  estudiantes_data = [
        {"codestudiante": estudiante.codestudiante, "nombre1": f"{estudiante.nombre1}", "nombre2": f"{estudiante.nombre2}",
         "apellido1": f"{estudiante.apellido1}", "apellido2": f"{estudiante.apellido2}"}
        for estudiante in estudiantes_grupo
    ]
  return JsonResponse(estudiantes_data, safe=False)
 
def cargarAsignaturas(request):
  estudiante_id = request.GET.get('estudiante') 
  inscribe_estudiante =Inscribe.objects.filter(codestudiante=estudiante_id)
  asignaturas_data = [
    {
        "codestudiante": inscribe.codestudiante.nombre1,  # Nombre del estudiante
        "codigoasignatura": f"{inscribe.codigoasignatura.codigoasignatura}",
        "Nombre": f"{inscribe.codigoasignatura.nombre}",
        "estudiante_id": inscribe.codestudiante.codestudiante  # Si necesitas el ID del estudiante
    }
    for inscribe in inscribe_estudiante
  ]

  return JsonResponse(asignaturas_data, safe=False)
 
def cargarNotas(request):
  estudiante_id = request.GET.get('estudiante') 
  asignatura_id = request.GET.get('asignatura') 
  asignatura = Asignatura.objects.get(codigoasignatura=asignatura_id)  
  notasEstudiante = Registronotas.objects.filter(codestudiante=estudiante_id, codigoasignatura=asignatura)
  
  notas_data = [
    {
        "parcial1": notas.parcial1, 
        "parcial2": notas.parcial2,
        "parcial3": notas.parcial3, 
        "parcial4": notas.parcial4, 
        "notafinal": notas.notafinal, 
    }
    for notas in notasEstudiante
  ]

  print("yepa")
  print(notas_data)
  return JsonResponse(notas_data, safe=False)
  
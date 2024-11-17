from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib import messages
from .forms import SeleccionGrupoAsignatura, AgregarEstudianteForm, InscribirForm, AsignarAulaForm, AgregarDocenteForm
from .models import Estudiante, Inscribe, Registronotas, Asignatura, Docente
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required


def loginView(request):
  if request.user.is_authenticated:
      return redirect('inicio')

  if request.method =="POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user  = authenticate(request,username=username, password=password)
    if user is None:
      messages.error(request, "No se encuentra al usuario")
      return render(request, "./login.html")
    else:
      messages.success(request, "Inicio de sesión exitoso")
      login(request, user)
      return redirect("inicio")
  else:   
    return render(request, "./login.html")

@login_required
def inicio(request):
    print(request.user.is_authenticated)
    print(request.user)
    return render(request, "./inicio.html")

@login_required
def registrarNotas(request):
    form = SeleccionGrupoAsignatura()
    
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

                defaults['parcial1'] = parcial1
                defaults['parcial2'] = parcial2
                defaults['parcial3'] = parcial3
                defaults['parcial4'] = parcial4
                defaults['notafinal'] = notafinal

                if defaults:

                    #busqueda = Registronotas.objects.get(codestudiante=estudiante, codigoasignatura=asignatura)
                    
                    print("busqueda")
                    #print(busqueda.codestudiante)
                    # Intenta actualizar o crear el registro utilizando `update_or_create`
                    registro, creado = Registronotas.objects.update_or_create(
                        codestudiante=estudiante,
                        codigoasignatura=asignatura,
                        periodoacademico=año_actual,
                        defaults=defaults
                    )
                    if creado:
                        messages.success(request, "Registro Creado")
                        
                    else:
                        messages.success(request, "Registro Actualizado")
        
            except Exception as e:
                messages.error(request, "Ha ocurrido un error")
                
                print(f"Error: {e}")
        
        return render(request, "./notas.html", {
            "form": form
        })
    
    else:
        return render(request, "./notas.html", {
            "form": form
        })
@login_required       
def AsignaturasAPI(request):
    asignaturas =Asignatura.objects.all()
   
    asignaturas_data = [
        {"codigoasignatura": asignatura.codigoasignatura, "nombre": f"{asignatura.nombre}",
         "idasignatura": f"{asignatura.idasignatura}"}
        for asignatura in asignaturas
    ]
    return JsonResponse(asignaturas_data, safe=False)


@login_required       
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

@login_required       
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

@login_required       
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
  return JsonResponse(notas_data, safe=False)

@login_required         
def EstudiantesAPI(request):
    estudiantes = Estudiante.objects.all()
    estudiantes_data = [
    {
        "codestudiante": est.codestudiante, 
        "nombre_completo": f"{est.nombre1} {est.nombre2} {est.apellido1} {est.apellido2}",
        "cédula": est.cedulaalumno,
        "codigogrupo": est.codigogrupo.nombre

    }
    for est in estudiantes
  ]
    return JsonResponse(estudiantes_data, safe=False)

@login_required       
def estudiantes(request):
            return render(request, "./EstudiantesModule/estudiante.html", {
        })

@login_required       
def infoEstudiante(request, codestudiante):
  EstudianteInfo = Estudiante.objects.get(codestudiante=codestudiante)
  return render(request, "./EstudiantesModule/infoEstudiante.html", {
    "Estudiante": EstudianteInfo
        })

@login_required       
def agregarEstudiante(request, codestudiante=None):
    if codestudiante:
        estudiante = get_object_or_404(Estudiante, codestudiante=codestudiante)
        form = AgregarEstudianteForm(request.POST or None, instance=estudiante)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante actualizado con éxito")
            return redirect('estudiantes') 
    else:
        form = AgregarEstudianteForm(request.POST or None)
        
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Estudiante Registrado con éxito")
            return redirect('estudiantes')  
    return render(request, './EstudiantesModule/agregarEstudiante.html', {'form': form, 'codestudiante': codestudiante})

@login_required       
def eliminarEstudiante(request, codestudiante):
    estudiante = get_object_or_404(Estudiante, codestudiante=codestudiante)
    
    if request.method == 'POST':
        estudiante.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@login_required       
def inscribirAsignaturas(request):
    if request.method == 'POST':
        form = InscribirForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.fechainscripcion = timezone.now()
            inscripcion.save()
            messages.success(request, 'Asignatura inscrita con éxito.')
            return redirect('inscripcionAsignatura')  # Redirigir a la misma vista después de la inscripción
        else:
            messages.error(request, 'Hubo un error al inscribir la asignatura.')
    else:
        form = InscribirForm()

    return render(request, './InscripcionModule/inscripcion.html', {'form': form})

@login_required       
def inscribirAula(request):
    if request.method == 'POST':
        form = AsignarAulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula asignada con éxito.')
            return render(request, "./inicio.html")
        else:
            # Acceder al error específico del campo `codigoaula` y pasarlo a mensajes
            if 'codigoaula' in form.errors:
                error_message = form.errors['codigoaula'][0]  # Obtener el primer error del campo `codigoaula`
                messages.error(request, error_message)
    else:
        form = AsignarAulaForm()
    form1 = AsignarAulaForm()
    return render(request, './AulasModule/aulas.html', 
                  {"form": form1})
@login_required       
def consultarNotas(request):
    return render(request, './ConsultarNotasModule/consultasnotas.html')

@login_required       
def consultarNotasAPI(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        codestudiante = data.get('codestudiante')
        
        try:
            estudiante = Estudiante.objects.get(codestudiante=codestudiante)
            notas = Registronotas.objects.filter(codestudiante=estudiante.codestudiante)
            notas_data = [
                {
                    'asignatura': nota.codigoasignatura.nombre, 
                    'parcial1': nota.parcial1,
                    'parcial2': nota.parcial2,
                    'parcial3': nota.parcial3,
                    'parcial4': nota.parcial4,
                    'nota_final': nota.notafinal,
                }
                for nota in notas
            ]

            return JsonResponse({'success': True, 'notas': notas_data})
        
        except Estudiante.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El estudiante no existe'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})
@login_required       
def gestionDocentes(request):
    return render(request, './GestionDocentesModule/docentes.html')


@login_required       
def DocentesAPI(request):
    docentes = Docente.objects.all()
    docentes_data = [
    {
        "ceduladocente": docente.ceduladocente, 
        "nombre": docente.nombre,
        "apellido": docente.apellido,
        "direccion": docente.direccion,
        "telefono": docente.telefono,
        "especialidad": docente.especialidad

    }
        for docente in docentes
    ]
    return JsonResponse(docentes_data, safe=False)

@login_required       
def infoDocente(request, ceduladocente):
  print("eeee ")
  DocenteInfo = Docente.objects.get(ceduladocente=ceduladocente)
  return render(request, "./GestionDocentesModule/infoDocente.html", {
    "DocenteInfo": DocenteInfo
        })

@login_required       
def agregarDocente(request, ceduladocente=None):
    if ceduladocente:
        docente = get_object_or_404(Docente, ceduladocente=ceduladocente)
        form = AgregarDocenteForm(request.POST or None, instance=docente)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Docente actualizado con éxito")
            return redirect('gestionDocentes') 
    else:
        form = AgregarDocenteForm(request.POST or None)
        
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Docente Registrado con éxito")
            return redirect('gestionDocentes')  
    return render(request, './GestionDocentesModule/agregarDocente.html', {'form': form, 'ceduladocente': ceduladocente})

@login_required        
def eliminarDocente(request, ceduladocente):
    docente = get_object_or_404(Docente, ceduladocente=ceduladocente)
    
    if request.method == 'POST':
        docente.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

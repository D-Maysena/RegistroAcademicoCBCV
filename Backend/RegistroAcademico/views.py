from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import SeleccionGrupoAsignatura, AgregarEstudianteForm, InscribirForm, AsignarAulaForm, AgregarDocenteForm, TutorForm, AsignarDocenteForm
from .models import Estudiante, Inscribe, Registronotas, Asignatura, Docente, Grupo, Turno, Aula, Asignacionaula, Tutor, Asignaciondocente
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required
from datetime import date

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
    #logout(request)
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
                notafinal = float(parcial1 +   parcial2 + parcial3 + parcial4) / 4
            else:
                notafinal = float(parcial1 +   parcial2 + parcial3 + parcial4) / 4
                

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
            "nombre_completo": f"{est.nombre1 or ''} {est.nombre2 or ''} {est.apellido1 or ''} {est.apellido2 or ''}".strip(),
            "cédula": est.cedulaalumno or "No disponible",
            "codigogrupo": est.codigogrupo.nombre if est.codigogrupo else "Sin grupo asignado"
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
def agregarTutor(request):
    if request.method == "POST":
        print("Método POST recibido")
        data = json.loads(request.body.decode("utf-8"))  # Leer datos como JSON
        Tutor = TutorForm(data)
        if Tutor.is_valid():
            print("Formulario Tutor es válido")
            tutor_instance = Tutor.save()
            return JsonResponse({
                "success": True,
                "message": "Tutor agregado exitosamente",
                "tutor_id": tutor_instance.codigotutor
            }, status=201)
        else:
            print("Formulario Tutor no es válido")
            return JsonResponse({
                "success": False,
                "errors": Tutor.errors,
                "message": "Error al agregar tutor"
            }, status=400)
    else:
        return JsonResponse({
            "success": False,
            "message": "Método no permitido, solo POST"
        }, status=405)



@login_required       
def agregarEstudiante(request, codestudiante=None):
    TutorF = TutorForm()

    if codestudiante:
        estudiante = get_object_or_404(Estudiante, codestudiante=codestudiante)
        form = AgregarEstudianteForm(request.POST or None, instance=estudiante)
    else:
        form = AgregarEstudianteForm(request.POST or None)
    
    if request.method == 'POST':    
        tutor = Tutor.objects.last()  # Esto recupera el último tutor agregado en la base de datos
        
        print("tutor")
        print(tutor)
        if form.is_valid():
            if codestudiante:   
                form.save()
                
                messages.success(request, "Estudiante actualizado con éxito")
                return redirect('estudiantes')
            else:
                grado = request.POST.get("grado")
                grupo = Grupo.objects.get(nivelacademico=grado)
                fomi = form.save(commit=False)
                fomi.codigogrupo = grupo
                
                asignacion_aula = Asignacionaula.objects.filter(codigogrupo=grupo).first()
                
                aula = asignacion_aula.codigoaula
                capacidad_aula = aula.capacidad
                
                estudiantes_inscritos = Estudiante.objects.filter(codigogrupo=grupo).count()
                print(estudiantes_inscritos)
                if estudiantes_inscritos >= capacidad_aula:
                    messages.error(request, "No se puede agregar más estudiantes. El aula ya ha alcanzado su capacidad máxima.")
                    return redirect('agregarEstudiante')  # Redirigir de nuevo al formulario
                
                if request.body.strip():  # Check if the body is not empty
                    try:
                        data = json.loads(request.body.decode("utf-8"))
                        is_button_enabled = data.get("is_button_enabled")
                 
                    except json.JSONDecodeError:
                        print("Error decoding JSON")
                else:
                    print("Empty body received")

                if tutor:
                    existing_tutor = Estudiante.objects.filter(codigotutor=tutor).exists()
                    if existing_tutor:
                        print("Este tutor ya está asignado a otro estudiante.")
                        messages.error(request, "Este tutor ya está asignado a otro estudiante.")
                    else:
                        fomi.codigotutor = tutor
                
                cedula = form.cleaned_data.get('cedulaalumno')
                if Estudiante.objects.filter(cedulaalumno=cedula).exists():
                    messages.error(request, "Ya existe un estudiante con esta cédula.")
                    return render(request, './EstudiantesModule/agregarEstudiante.html', {
                            'form': form,
                            'codestudiante': codestudiante,
                            'tutorform': TutorF
                            })
                fecha_nac = fomi.fechanac
                if fecha_nac:
                    # Calcular la edad si se proporciona la fecha de nacimiento
                    edad = calcular_edad(fecha_nac)
                    fomi.edad = edad
                    fomi.save()
                estudiantegregado = fomi.codestudiante
                messages.success(request, "Estudiante registrado con éxito")
                return redirect('agregar2', estudiantegregado)
        else:
            # Si hay errores, combinar los errores de ambos formularios para mostrarlos
            error_messages = []

            if form.errors:
                error_messages.append(' '.join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]))
          

            combined_error_message = ' '.join(error_messages)
            messages.error(request, combined_error_message)

    return render(request, './EstudiantesModule/agregarEstudiante.html', {
        'form': form,
        'codestudiante': codestudiante,
        'tutorform': TutorF
    })

def calcular_edad(fecha_nac):
    """Calcula la edad de un estudiante a partir de su fecha de nacimiento"""
    # Convertir la fecha de nacimiento de cadena a objeto datetime
    fecha_nac_obj = datetime.strptime(fecha_nac, "%Y-%m-%d")  # Ajusta el formato si es diferente

    print(fecha_nac_obj.day)  # Ahora esto funcionará
    fecha_actual = datetime.now()

    # Calcular la edad
    edad = fecha_actual.year - fecha_nac_obj.year
    if (fecha_actual.month, fecha_actual.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
        edad -= 1

    return edad

def agregar2(request, estudiantegregado):
    estudiante = Estudiante.objects.get(codestudiante=estudiantegregado)

    grupo = estudiante.codigogrupo
    asignaturas = Asignatura.objects.filter(codigogrupo=grupo.codigogrupo)
  
    asignaturasEstudiante = [
        {
            'idasignatura': asignatura.idasignatura, 
            'nombre': asignatura.nombre,       
        }
        for asignatura in asignaturas
    ]
    print(estudiante.codigogrupo.nombre) 

    aula = Asignacionaula.objects.get(codigogrupo=grupo.codigogrupo)
    print(aula.codigoaula)
    if request.method == 'POST':
            for asignatura in asignaturas:
                if not Inscribe.objects.filter(codestudiante=estudiante, codigoasignatura=asignatura).exists():
                    Inscribe.objects.create(
                    codestudiante=estudiante,
                    codigoasignatura=asignatura,
                    fechainscripcion=date.today()
                )
            messages.success(request, "Estudiante matriculado con éxito")
            return redirect('inicio')
                    
        
    return render(request,"./EstudiantesModule/agregar2.html",{
    "asignaturas": asignaturasEstudiante,
    "grupo": estudiante.codigogrupo,
    "aula": aula,
    "codestudiante": estudiante.codestudiante
    })  


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
            # Obtener el código del aula desde el formulario
            codigo_aula = form.cleaned_data['codigoaula']
            print(codigo_aula)
            # Verificar si ya existe una asignación con ese código
            if Aula.objects.filter(codigoaula=codigo_aula.codigoaula).exists():  # Cambia 'Aula' y 'codigoaula' según tu modelo
                messages.error(request, f'El aula con código {codigo_aula} ya está asignada.')
                return render(request, './AulasModule/aulas.html', {"form": form})
            
            # Si no existe, guardar la asignación
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
    
    # Crear un nuevo formulario para la vista, en caso de que se necesite
    form1 = AsignarAulaForm()
    
    return render(request, './AulasModule/aulas.html', {"form": form1})

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
        
        if request.method == "POST":
            if form.is_valid():
                # Validar que la cédula no exista ya en la base de datos
                cedula_nueva = form.cleaned_data.get('ceduladocente')
                if Docente.objects.filter(ceduladocente=cedula_nueva).exists():
                    messages.error(request, "La cédula ya está registrada.")
                else:
                    form.save()
                    messages.success(request, "Docente registrado con éxito")
                    return redirect('gestionDocentes')
            else:
                messages.error(request, "Por favor, corrige los errores en el formulario.")
    
    return render(request, './GestionDocentesModule/agregarDocente.html', {'form': form, 'ceduladocente': ceduladocente})
@login_required        
def eliminarDocente(request, ceduladocente):
    docente = get_object_or_404(Docente, ceduladocente=ceduladocente)
    
    if request.method == 'POST':
        docente.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


def asignarDocente(request):
    # Crear una instancia del formulario
    asig = AsignarDocenteForm()

    if request.method == "POST":
        # Volver a cargar el formulario con los datos POST
        asig = AsignarDocenteForm(request.POST)

        # Verificar si el formulario es válido
        if asig.is_valid():
            # Extraer los datos del formulario
            cedula_docente = asig.cleaned_data['ceduladocente']
            codigo_grupo = asig.cleaned_data['codigogrupo']

            # Verificar si ya existe una asignación con el mismo docente y grupo
            if Asignaciondocente.objects.filter(ceduladocente=cedula_docente, codigogrupo=codigo_grupo).exists():
                messages.error(request, "Este docente ya está asignado a este grupo.")
            else:
                # Si no existe la asignación, guardar los datos
                asig.save()
                messages.success(request, "Docente asignado con éxito")
                return redirect('asignarDocente')  # Redirige a la lista de docentes (o donde desees)
        
        else:
            # Si el formulario no es válido, imprimir los errores
            print(asig.errors)
            messages.error(request, "Hubo un error al asignar el docente. Verifique los datos.")
    
    return render(request, "./GestionDocentesModule/AsignarDocente.html", {
        "form": asig
    })
    
    
def horarios(request):
    asignaciones_aula = Asignacionaula.objects.all()
    
    horario = []
    
    for asignacion in asignaciones_aula:
        grupo = asignacion.codigogrupo
        aula = asignacion.codigoaula
        turno = asignacion.codigoturno
        
        # Buscar el docente asignado al grupo
        asignacion_docente = Asignaciondocente.objects.filter(codigogrupo=grupo).first()
        print(asignacion_docente)
        docente = asignacion_docente.ceduladocente if asignacion_docente else None
        
        horario.append({
            'grupo': grupo.nombre if grupo else 'No asignado',
            'aula': aula.numeroaula if aula else 'No asignada',
            'turno': turno.horario if turno else 'No asignado',
            'docente': f"{docente.nombre} {docente.apellido}" if docente else "No asignado",
        })
    
    return render(request, './horarios.html', {
        'horario': horario
    })
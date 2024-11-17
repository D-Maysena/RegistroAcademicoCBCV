from django import forms
from .models import Asignatura, Grupo, Estudiante, Inscribe, Aula, Asignacionaula, Turno, Docente

class SeleccionGrupoAsignatura(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(), 
        label="Seleccione el grupo",
        widget=forms.Select(attrs={'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        label="Selecciona al estudiante",
         widget=forms.Select(attrs={'class': 'form-control'}))
    Asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        label="Seleccione la asignatura",
        widget=forms.Select(attrs={'class': 'form-control'}))
    
class AgregarEstudianteForm(forms.ModelForm):
    
    class Meta:
        model = Estudiante
        SEXO_CHOICES = [
            ('M', 'Masculino'),
            ('F', 'Femenino'),
        ]
        fields = [
            'codestudiante', 'nombre1', 'nombre2', 'apellido1', 'apellido2',
            'fechanac', 'sexo', 'cedulaalumno', 'direccionalumno', 'matricula', 
            'codigogrupo', 'codigotutor'
        ]
        
        labels = {
            'codestudiante': "Código de Estudiante",
            'nombre1': "Primer Nombre",
            'nombre2': "Segundo Nombre",
            'apellido1': "Primer Apellido",
            'apellido2': "Segundo Apellido",
            'fechanac': "Fecha de Nacimiento",
            'sexo': "Sexo",
            'cedulaalumno': "Cédula del Alummno ",
            'direccionalumno': "Dirección",
            'matricula': "Matricula",
            'codigogrupo': "Código de Grupo",
            'codigotutor': "Código de Tutor",
        }
        
        widgets = {
            'codestudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre1': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre2': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
            'fechanac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(choices=SEXO_CHOICES, attrs={'class': 'form-control'}),
            'cedulaalumno': forms.TextInput(attrs={'class': 'form-control'}),
            'direccionalumno': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'codigogrupo': forms.Select(attrs={'class': 'form-control'}),
            'codigotutor': forms.TextInput(attrs={'class': 'form-control'})
        }
        
class InscribirForm(forms.ModelForm):
    class Meta:
        model = Inscribe
        fields = [
            'codestudiante', 'codigoasignatura'
        ]
        labels = {
            'codestudiante': "Código de Estudiante",
            'codigoasignatura': "Código de Asignatura",
        }
        widgets = {
            'codestudiante': forms.Select(attrs={'class': 'form-control custom-select'}),
            'codigoasignatura': forms.Select(attrs={'class': 'form-control custom-select'}),
        }
        
class AsignarAulaForm(forms.ModelForm):
    class Meta:
        model = Asignacionaula
        fields = [
            'codigoaula', 'codigogrupo', 'codigoturno'
        ]
        labels = {
            'codigoaula': "Código de Aula",
            'codigogrupo': "Código de Grupo",
            'codigoturno': "Código de Turno",
        }
        widgets = {
            'codigoaula': forms.Select(attrs={'class': 'form-control custom-select'}),
            'codigogrupo': forms.Select(attrs={'class': 'form-control custom-select'}),
            'codigoturno': forms.Select(attrs={'class': 'form-control custom-select'}),
        }
        
        
class AgregarDocenteForm(forms.ModelForm):
    
    class Meta:
        model = Docente

        fields = [
            'ceduladocente', 'nombre', 'apellido', 'telefono',
            'especialidad', 'direccion'
        ]
        
        labels = {
            'ceduladocente': "Código de Estudiante",
            'nombre': "Primer Nombre",
            'apellido': "Segundo Nombre",
            'telefono': "Teléfono",
            'especialidad': "Especialidad",
            'direccion': "Direccion",
        }
        
        widgets = {
            'ceduladocente': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre2': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),  
            'direccion': forms.TextInput(attrs={'class': 'form-control'}), 
        }

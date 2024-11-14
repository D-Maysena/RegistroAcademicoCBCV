from django import forms
from .models import Asignatura, Grupo, Estudiante

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
        SEXO_CHOICES = [
            ('M', 'Masculino'),
            ('F', 'Femenino'),
        ]
        model = Estudiante
        fields = [
            'codestudiante', 'nombre1', 'nombre2', 'apellido1', 'apellido2',
            'fechanac', 'sexo', 'cedulaalumno', 'direccionalumno', 'matricula', 
            'codigogrupo', 'codigotutor'
        ]
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
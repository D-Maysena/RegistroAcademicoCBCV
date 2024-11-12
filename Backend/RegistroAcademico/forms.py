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
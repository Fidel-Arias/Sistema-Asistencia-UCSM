from django import forms
from .models import MaeUbicacion

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = MaeUbicacion
        fields = ['idubicacion', 'ubicacion']
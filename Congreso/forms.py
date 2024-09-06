from django import forms
from .models import MaeCongreso

class CongresoJinisForm(forms.ModelForm):
    class Meta:
        model = MaeCongreso
        fields = ['idcongreso', 'nombre', 'fechainicio', 'fechafin', 'asistenciatotal']
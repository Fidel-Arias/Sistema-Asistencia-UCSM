from django import forms
from .models import MaePonencia

class PonenciaForm(forms.ModelForm):
    class Meta:
        model = MaePonencia
        fields = ['idponencia', 'idponente', 'nombre', 'idcongreso']
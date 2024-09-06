from django import forms
from .models import MaePonente

class PonenteForm(forms.ModelForm):
    class Meta:
        model = MaePonente
        fields = ('idponente', 'nombres', 'apellidos')
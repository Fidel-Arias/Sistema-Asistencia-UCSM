from django import forms
from .models import MaeBloque

class BloqueForm(forms.ModelForm):
    class Meta:
        model = MaeBloque
        fields = ['idbloque', 'idponencia', 'iddia', 'horainicio', 'horafin', 'idubicacion']
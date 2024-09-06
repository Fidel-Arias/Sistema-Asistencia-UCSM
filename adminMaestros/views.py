from django.shortcuts import render
from .models import AdministradorCongreso
from Admin.models import MaeAdministrador
from Congreso.models import MaeCongreso

# Create your views here.
def administrador_congreso(data):
    try:
        administrador = MaeAdministrador.objects.get(correo=data['correo'])
        congreso = MaeCongreso.objects.get(pk = data['idcongreso'])
        if not AdministradorCongreso.objects.filter(idadministrador=administrador.pk).exists():
            administrador_congreso = AdministradorCongreso(idadministrador = administrador, idcongreso = congreso)
            administrador_congreso.save()
            return True
        else:
            return False
    except MaeAdministrador.DoesNotExist:
        return False
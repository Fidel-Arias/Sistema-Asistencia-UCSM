from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.shortcuts import render
from Admin.models import MaeAdministrador

class Interfaz_Administrador(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def interfaz_administrador(self, request, pk):
        admin = MaeAdministrador.objects.get(pk=pk)
        return render(request, 'interfazBienvenida.html', {
            'pk': pk,
            'admin': admin
        })
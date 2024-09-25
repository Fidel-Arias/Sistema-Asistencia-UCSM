from django.shortcuts import render, redirect
from django.urls import reverse
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.db import transaction
from adminMaestros.models import AdministradorBloquecolaborador, AdministradorCongreso, AdministradorColaborador, AdministradorBloques
from Admin.models import MaeAdministrador
from Bloque.models import MaeBloque
from Colaborador.models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from django.contrib import messages

class Registrar_Asistencia_por_Fallas(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_asistencia(self, request, pk):
        if request.method == 'POST':
            colaborador = request.POST.get('colaborador')
            bloque = request.POST.get('bloque')
            falla = request.POST.get('falla')
            observaciones = request.POST.get('observaciones')
        else:
            return render(request, 'pages/registrar_asistencia.html', {
                'current_page': 'registrar_asistencia',
                'pk': pk
            })
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from Participantes.decorators import participante_login_required
from Participantes.models import MaeParticipantes
from adminMaestros.models import AdministradorBloques
from ParticipanteCongreso.models import ParticipanteCongreso
from adminMaestros.models import AdministradorCongreso
from datetime import datetime

# Create your views here.
class viewPonencias(viewsets.ViewSet):
    @method_decorator(participante_login_required)
    def verPonencias(self, request, pk):
        try:
            codparticipante = request.session.get('codparticipante')
            if codparticipante != str(pk):
                request.session['error'] = 'Acceso inválido'
                return redirect('Login')  # Redirigir si no está autenticado o si intenta acceder a otro usuario

            congreso = ParticipanteCongreso.objects.get(codparticipante=pk)
            admin = AdministradorCongreso.objects.get(idcongreso=congreso.idcongreso)
            bloques = AdministradorBloques.objects.filter(idadministrador = admin.idadministrador)
            participante = MaeParticipantes.objects.get(pk=pk)
            fecha_actual = datetime.now().strftime('%d/%m/%Y')
            return render(request, 'ponencias.html', {
                'ponencias': bloques,
                'participante': participante,
                'fecha_actual': fecha_actual
            })
        except Exception:
            return render(request, 'ponencias.html')
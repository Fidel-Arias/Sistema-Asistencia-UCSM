from Participantes.models import MaeParticipantes
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.urls import reverse
from email_service.views import email_service
from decorators import administrador_login_required
from models import MaeAdministrador
from adminMaestros.models import AdministradorCongreso
from datetime import datetime

class EnviarFormulario(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def enviar_formulario(self, request, pk):
        admin = MaeAdministrador.objects.get(pk=pk)
        admin_congreso = AdministradorCongreso.objects.get(idadministrador=pk)
        datos_admin = {
            'correo': admin.correo,
            'contrasenia': request.session.get('contrasenia_admin'),
        }
        if request.method == 'POST':
            try:
                participantes = MaeParticipantes.objects.all()
                link_formulario = request.POST.get('link-form')
                for participante in participantes:
                    correo = participante.correo
                    enviar_email_formulario(request, datos_admin, correo, None, admin_congreso.idcongreso.nombre, link_formulario)
                
                messages.success(request, 'Formulario enviado correctamente a todos los participantes')
                return redirect(reverse('GenerarReporte', kwargs={'pk':pk}))
            except Exception as e:
                print('Error: ', e)
                messages.error(request, 'Error al enviar el formulario a todos los participantes')
                return redirect(reverse('GenerarReporte', kwargs={'pk':pk}))
        


def enviar_email_formulario(request, datos_admin, correos, img_path, congreso, link_formulario):
    try:
        template = render_to_string('messages/mail_formulario.html', {
            'congreso': congreso,
            'url': link_formulario
        })
        plain_message = f"ENCUESTA DE SATISFACCION - {congreso} 2024. Estimado, realice la siguiente encuesta de satisfacción para el {congreso} 2024. Ingresa al siguiente link: {link_formulario}"

        subject = f"ENCUESTA DE SATISFACCIÓN - {congreso} {datetime.now().year}"

        status_email = email_service(request, datos_admin, template, plain_message, subject, correos, img_path)

        return status_email
    except Exception:
        return 'failed'
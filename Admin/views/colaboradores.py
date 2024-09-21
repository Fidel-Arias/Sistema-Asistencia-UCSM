from django.shortcuts import render, redirect
from django.db import transaction
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.template.loader import render_to_string
from adminMaestros.models import AdministradorCongreso
from adminMaestros.models import AdministradorColaborador
from Admin.models import MaeAdministrador
from tipoUsuario.models import MaeTipousuario
from Colaborador.models import MaeColaborador
from Colaborador.forms import ColaboradorForm
from tipoUsuario.models import MaeTipousuario
from ..decorators import administrador_login_required
from email_service.views import email_service
from django.contrib import messages
from config import settings

class Registrar_Colaboradores(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_colaboradores(self, request, pk):
        admin = MaeAdministrador.objects.get(pk=pk)
        datos_admin = {
            'correo': admin.correo,
            'contrasenia': request.session.get('contrasenia_admin')
        }
        if request.method == 'POST':
            idTipoUsuario = request.POST.get('tipoUsuario')
            nombres = request.POST.get('nombre')
            apellidos = request.POST.get('apellido')
            correo = request.POST.get('correo')
            contrasenia = request.POST.get('contrasenia')
            action = request.POST.get('action')
            congreso = AdministradorCongreso.objects.get(idadministrador=pk)

            colaborador_data = {
                    'nombres_admin': admin.nombres + ' ' + admin.apellidos,
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'correo': correo,
                    'contrasenia': contrasenia,
                    'idTipoUsuario': MaeTipousuario.objects.get(pk=idTipoUsuario).dstipo,
                    'nombreCongreso': congreso.idcongreso.nombre
                }
            

            if action == 'register':
                try:
                    if (not(MaeColaborador.objects.filter(nombres=nombres, apellidos=apellidos).exists())):
                        with transaction.atomic():
                            nuevo_colaborador = MaeColaborador(
                                nombres=nombres,
                                apellidos=apellidos,
                                correo=correo,
                                contrasenia=contrasenia,
                                idtipo=MaeTipousuario.objects.get(pk=idTipoUsuario),
                            )
                            nuevo_colaborador.save()

                            #Asociando el colaborador a la tabla administrador
                            admin_colaborador = AdministradorColaborador(
                                idadministrador=admin,
                                idcolaborador=nuevo_colaborador,
                            )
                            admin_colaborador.save()

                        #ENVIAR DATOS AL SERVICIO EMAIL
                        template_or_message = crear_template_or_message(request, colaborador_data)
                        subject = f"Selección para colaborador en el congreso {colaborador_data['nombreCongreso']}"
                        
                        if template_or_message:
                            status_email = email_service(request, datos_admin, template_or_message[0], template_or_message[1], subject, [colaborador_data['correo']])

                            if status_email == 'failed':
                                messages.error(request, 'No se pudo enviar el correo al destino')
                                return redirect(reverse('RegistrarColaboradores', kwargs={'pk':pk}))
                        else:
                            messages.error(request, 'No se pudo construir el template')

                        messages.success(request, 'Colaborador registrado con éxito')
                    else:
                        messages.error(request, 'El colaborador registrado ya existe')
                except Exception as e:
                    messages.error(request, 'Error al registrar colaborador')
            elif action == 'delete':
                try:
                    colaborador = MaeColaborador.objects.get(nombres=nombres, apellidos=apellidos)
                    #ELIMINACION TOTAL
                    '''colaborador.delete()'''
                    #ELIMINACION LOGICA
                    colaborador.estado = "NO ACTIVO"
                    colaborador.save()
                    messages.success(request, 'El colaborador ha sido desactivado con éxito')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception:
                    messages.error(request, 'Error al desactivar al colaborador')
            elif action == 'activate':
                try:
                    colaborador = MaeColaborador.objects.get(nombres=nombres, apellidos=apellidos)
                    colaborador.estado = "ACTIVO"
                    colaborador.save()
                    messages.success(request, 'El colaborador ha sido activado con éxito')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception:
                    messages.error(request, 'Error al activar al colaborador')
            elif action == 'edit':
                idcolaborador = request.POST.get('id')
                try:
                    colaborador = MaeColaborador.objects.get(pk=idcolaborador)
                    contexto = {
                        'nombres': nombres,
                        'apellidos': apellidos,
                        'correo': correo,
                        'contrasenia': contrasenia,
                        'idtipo': MaeTipousuario.objects.get(idtipo=idTipoUsuario),
                    }
                    colaborador_actualizado = ColaboradorForm(contexto, instance=colaborador)
                    if colaborador_actualizado.is_valid():
                        colaborador_actualizado.save()
                        messages.success(request, 'El colaborador se ha actualizado con éxito')
                    else:
                        messages.error(request, 'Error al actualizar al colaborador')
                except MaeColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador')
                except Exception as e:
                    messages.error(request, e)

            return redirect(reverse('RegistrarColaboradores', kwargs={'pk':pk}))
        else:
            colaboradores = AdministradorColaborador.objects.filter(idadministrador=pk)
            tiposUsuario = MaeTipousuario.objects.filter(dstipo='COLABORADOR')
            return render(request, 'pages/registrarColaboradores.html', {
                'current_page':'registrar_colaboradores', 
                'colaboradores':colaboradores, 
                'tiposUsuario':tiposUsuario, 
                'pk': pk
            })
        
def crear_template_or_message(request, data_user):
    try:
        url_colaborador = settings.DOMAIN_URL + reverse('LoginColaborador')
        template = render_to_string('messages/mail_colaborador.html', {
            'nombres_admin': data_user['nombres_admin'],
            'nombre': f"{data_user['nombres']} {data_user['apellidos']}",
            'nombre_congreso': data_user['nombreCongreso'],
            'correo': data_user['correo'],
            'contrasenia': data_user['contrasenia'],
            'enlace_colaborador': url_colaborador,
            'Tipo': data_user['idTipoUsuario'],
        })

        plain_message = f"Nuevo Colaborador: {data_user['nombres']} {data_user['apellidos']}\nCongreso: {data_user['nombreCongreso']}\nTu Correo: {data_user['correo']}\nTu contraseña: {data_user['contrasenia']}\n"

        return template, plain_message
    except Exception as e:
        print('Error creando template: ', e)
        return None
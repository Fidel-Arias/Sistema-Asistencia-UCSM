from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.urls import reverse
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from adminMaestros.models import AdministradorCongreso, AdministradorPonencias, AdministradorPonentes
from Admin.models import MaeAdministrador
from Ponente.models import MaePonente
from Ponencia.models import MaePonencia
from Ponencia.forms import PonenciaForm
from Ponente.models import MaePonente
from Congreso.models import MaeCongreso
from django.contrib import messages
from django.db import transaction

class Registrar_Ponencias(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_ponencias(self, request, pk):
        if request.method == 'POST':
            action = request.POST.get('action')
            ponente = request.POST.get('ponente')
            nombrePonencia = request.POST.get('nombre_ponencia')
            admin = AdministradorCongreso.objects.get(idadministrador = pk)

            if action == 'register':
                try:
                    if (not(MaePonencia.objects.filter(nombre=nombrePonencia).exists())):
                        with transaction.atomic():
                            nueva_ponencia = MaePonencia(
                                nombre=nombrePonencia,
                                idponente=MaePonente.objects.get(pk=ponente),
                                idcongreso=MaeCongreso.objects.get(pk=admin.idcongreso.pk)
                            )
                            nueva_ponencia.save()
                            admin_ponencia = AdministradorPonencias(
                                idadministrador=admin.idadministrador,
                                idponencia=nueva_ponencia
                            )
                            admin_ponencia.save()
                        messages.success(request, 'Ponencia registrada con éxito')
                    else:
                        messages.error(request, 'Ya existe la ponencia')
                except Exception as e:
                    print('Error: ', e)
                    messages.error(request, 'Error al registrar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'delete':
                try:
                    ponencia = MaePonencia.objects.get(nombre=nombrePonencia)
                    #ELIMINACION TOTAL
                    '''ponencia.delete()'''
                    #ELIMINACION LOGICA
                    ponencia.estado = 'NO ACTIVO'
                    ponencia.save()
                    messages.success(request, 'Ponencia desactivada con éxito')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al desactivar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'activate':
                idponencia = request.POST.get('id')
                try:
                    ponencia = MaePonencia.objects.get(pk=idponencia)
                    #ELIMINACION TOTAL
                    '''ponencia.delete()'''
                    #ELIMINACION LOGICA
                    ponencia.estado = 'ACTIVO'
                    ponencia.save()
                    messages.success(request, 'Ponencia activada con éxito')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al activar la ponencia')
                return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
            elif action == 'edit':
                idponencia = request.POST.get('id')
                print('Ponente', ponente)
                try:
                    ponencia = MaePonencia.objects.get(pk=idponencia)
                    contexto = {
                        'idponente': ponente,
                        'nombre': nombrePonencia,
                        'idcongreso': MaeCongreso.objects.get(pk=admin.idcongreso.pk)
                    }
                    ponencia_actualizada = PonenciaForm(contexto, instance=ponencia)
                    if ponencia_actualizada.is_valid():
                        ponencia_actualizada.save()
                        messages.success(request, 'Ponencia actualizada con éxito')
                    else:
                        messages.error(request, 'Error al actualizar la ponencia')
                except MaePonencia.DoesNotExist:
                    messages.error(request, 'No se encontró la ponencia')
                except Exception:
                    messages.error(request, 'Error al actualizar la ponencia')
            
            return redirect(reverse('RegistrarPonencia', kwargs={'pk':pk}))
        else:
            try:
                ponentes_activos = MaePonente.objects.filter(estado="ACTIVO")
                admin_ponentes = MaeAdministrador.objects.prefetch_related(
                    Prefetch('administradorponentes_set', queryset=AdministradorPonentes.objects.filter(
                        idponente__in=ponentes_activos
                    ))
                ).filter(pk=pk)

                ponencias = AdministradorPonencias.objects.filter(idadministrador = pk).order_by('pk')
                return render(request, 'pages/registrarPonencia.html', {
                    'current_page': 'registrar_ponencia', 
                    'ponentes_activos': ponentes_activos,
                    'ponencias': ponencias, 
                    'admin_ponentes': admin_ponentes, 
                    'pk':pk
                })
            except Exception as e:
                print('Error: ', e)
                ponencias = AdministradorPonencias.objects.filter(idadministrador = pk).order_by('pk')
                messages.error(request, 'Error al cargar los ponentes')
                return render(request, 'pages/registrarPonencia.html', {
                    'current_page': 'registrar_ponencia', 
                    'ponencias': ponencias, 
                    'pk':pk
                })
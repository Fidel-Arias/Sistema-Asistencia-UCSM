from django.db import connection
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from ..decorators import administrador_login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.db import transaction
from Admin.models import MaeAdministrador
from Bloque.models import MaeBloque
from Bloque.forms import BloqueForm
from Ponencia.models import MaePonencia
from Dia.models import MaeDia
from Congreso.models import MaeCongreso
from Ubicacion.models import MaeUbicacion
from django.contrib import messages
from adminMaestros.models import AdministradorCongreso, AdministradorBloques, AdministradorPonencias

class Registrar_Bloques(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_bloques(self, request, pk):
        if request.method == 'POST':
            ponencia = request.POST.get('ponencia')
            dia = request.POST.get('dia')
            horaInicio = request.POST.get('hora_inicio')
            horaFin = request.POST.get('hora_fin')
            ubicacion = request.POST.get('ubicacion')
            action = request.POST.get('action')
            admin = AdministradorCongreso.objects.get(idadministrador=pk)
            
            if action == 'register':
                if not MaeBloque.objects.filter(idponencia=ponencia).exists():
                    try:
                        if horaInicio == horaFin:
                            messages.error(request, "La hora inicial y final deben ser diferentes")
                        elif horaFin < horaInicio:
                            messages.error(request, "La hora inicial no puede ser mayor a la hora final")
                        else:
                            resultado = verificar_ubicacion(0, dia, horaInicio, horaFin, ubicacion)
                            print('resultado: ' ,resultado)
                            if resultado == 'OK':
                                with transaction.atomic():
                                    nuevo_bloque = MaeBloque(
                                        idponencia=MaePonencia.objects.get(pk=ponencia),
                                        iddia= MaeDia.objects.get(pk=dia),
                                        horainicio=horaInicio,
                                        horafin=horaFin,
                                        idubicacion=MaeUbicacion.objects.get(pk=ubicacion)
                                    )
                                    nuevo_bloque.save()
                                    admin_bloque = AdministradorBloques(
                                        idadministrador = admin.idadministrador,
                                        idbloque = nuevo_bloque
                                    )
                                    admin_bloque.save()
                                messages.success(request, "El bloque ha sido creado exitosamente")
                            else:
                                messages.error(request, "El auditorio no esta disponible para la hora indicada")
                    except Exception:
                        messages.error(request, 'Se produjo un error al crear el bloque')
                else:
                    messages.error(request, "Ya existe una ponencia en los bloques")
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'delete':
                try:
                    bloque = MaeBloque.objects.get(idponencia=ponencia, iddia=dia, horainicio=horaInicio, horafin=horaFin, idubicacion=ubicacion)
                    #ELIMINACION TOTAL
                    '''bloque.delete()'''
                    #ELIMINACION LOGICA
                    bloque.estado = "NO ACTIVO"
                    bloque.save()
                    messages.success(request, 'El bloque ha sido desactivado exitosamente')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al desactivar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'activate':
                try:
                    bloque = MaeBloque.objects.get(idponencia=ponencia, iddia=dia, horainicio=horaInicio, horafin=horaFin, idubicacion=ubicacion)
                    bloque.estado = "ACTIVO"
                    bloque.save()
                    messages.success(request, 'El bloque ha sido activado exitosamente')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al activar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
            elif action == 'edit':
                idbloque = request.POST.get('id');
                try:
                    bloque = MaeBloque.objects.get(pk=idbloque)
                    contexto = {
                        'idponencia': ponencia,
                        'iddia': dia,
                        'horainicio': horaInicio,
                        'horafin': horaFin,
                        'idubicacion': ubicacion
                    }
                    bloque_actualizado = BloqueForm(contexto, instance=bloque)
                    if bloque_actualizado.is_valid():
                        bloque_actualizado.save()
                        messages.success(request, 'El bloque ha sido actualizado exitosamente')
                    else:
                        messages.error(request, 'Se produjo un error al actualizar el bloque')
                except MaeBloque.DoesNotExist:
                    messages.error(request, 'El bloque no existe')
                except Exception:
                    messages.error(request, 'Se produjo un error al actualizar el bloque')
                return redirect(reverse('RegistrarBloques', kwargs={'pk':pk}))
        else:
            try: 
                bloques = AdministradorBloques.objects.filter(idadministrador=pk)
                admin = AdministradorCongreso.objects.get(idadministrador = pk)
                lista_dias = MaeDia.objects.filter(idcongreso=admin.idcongreso, estado='ACTIVO').order_by('pk')
                
                #APLICANDO EL ORM
                ponencias_activas = MaePonencia.objects.filter(idcongreso=admin.idcongreso, estado='ACTIVO')
                admin_ponencias = MaeAdministrador.objects.prefetch_related(
                    Prefetch('administradorponencias_set', queryset=AdministradorPonencias.objects.filter(
                        idponencia__in = ponencias_activas
                    ))
                ).filter(pk=pk)

                ubicaciones = MaeUbicacion.objects.filter(estado='ACTIVO').order_by('pk')
                #VALIDACIONES
                if not AdministradorPonencias.objects.filter(idadministrador=pk).exists():
                    messages.warning(request,'No hay ponencias registradas, por favor registre al menos una')
                elif not MaeDia.objects.filter(idcongreso=admin.idcongreso).exists() or not MaeDia.objects.filter(estado='ACTIVO').exists():
                    messages.warning(request, 'No hay días registrados o activos, por favor registre al menos un día')
                elif not MaeUbicacion.objects.filter(estado='ACTIVO').exists() or not MaeUbicacion.objects.filter().exists():
                    messages.warning(request, 'No hay ubicaciones registradas o activas, por favor registre al menos una ubicación')
                
                return render(request, 'pages/registrarBloques.html', {
                    'current_page': 'registrar_bloques', 
                    'bloques':bloques, 
                    'ponencias_activas': ponencias_activas, 
                    'admin_ponencias': admin_ponencias,
                    'dias': lista_dias, 
                    'ubicaciones':ubicaciones, 
                    'pk': pk
                })
            except Exception as e:
                print('error: ', e)
                messages.error(request, 'Ha ocurrido un error al cargar las ponencias')
                return render(request, 'pages/registrarBloques.html', {
                    'current_page': 'registrar_bloques', 
                    'pk': pk
                })

def verificar_ubicacion(id, fecha, hora_inicio, hora_fin, ubicacion):
    cursor = connection.cursor()
    cursor.callproc('verificar_ubicacion', [id, fecha, hora_inicio, hora_fin, ubicacion])
    resultado = cursor.fetchone()[0]
    return resultado
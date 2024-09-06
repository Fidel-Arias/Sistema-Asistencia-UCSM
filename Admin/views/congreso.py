from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from Congreso.models import MaeCongreso
from Congreso.forms import CongresoJinisForm
from adminMaestros.models import AdministradorCongreso
from Dia.models import MaeDia
from django.contrib import messages
from datetime import date
import pandas as pd

class Registrar_Congreso(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_congreso(self, request, pk):
        if request.method == 'POST':
            action = request.POST.get('action')
            nombreCongreso = request.POST.get('nombreCongreso')
            fechaHoy = date.today()
            fechaInicio = request.POST.get('fechaInicio')
            fechaFin = request.POST.get('fechaFin')
            asistenciaTotal = request.POST.get('totalAsistencia')

            if action == 'desactivate':
                try:
                    congreso = MaeCongreso.objects.get(nombre=nombreCongreso)
                    #ELIMINACION TOTAL
                    '''congreso.delete()'''
                    #ELIMINACION LOGICA
                    congreso.estado = 'NO ACTIVO'
                    congreso.save()
                    desactivarDias(request, congreso.idcongreso, pk)
                    messages.success(request, 'Congreso desactivado con éxito')
                except MaeCongreso.DoesNotExist:
                    messages.error(request, 'No se encontró el congreso')
                except Exception as e:
                    messages.error(request, e)
            elif action == 'activate':
                try:
                    congreso = MaeCongreso.objects.get(nombre=nombreCongreso)
                    congreso.estado = 'ACTIVO'
                    congreso.save()
                    activarDias(request, congreso.idcongreso, pk)
                    messages.success(request, 'Congreso activado con éxito')
                except MaeCongreso.DoesNotExist:
                    messages.error(request, 'No se encontró el congreso')
                except Exception:
                    messages.error(request, 'Error al activar el congreso')
            elif action == 'edit':
                idcongreso = request.POST.get('id')
                if fechaInicio == fechaFin:
                    messages.error(request, 'Las fechas de inicio y fin deben ser distintas')
                elif fechaFin < fechaInicio:
                    messages.error(request, 'Ingrese correctamente las fechas')
                elif fechaInicio < fechaHoy.__str__() or fechaFin < fechaHoy.__str__():
                    messages.error(request, 'La fecha de inicio y fin no puede ser anterior a la fecha de hoy')
                try:
                    congreso = MaeCongreso.objects.get(pk=idcongreso)
                    contexto = {
                        'nombre': nombreCongreso,
                        'fechainicio': fechaInicio,
                        'fechafin': fechaFin,
                        'asistenciatotal': asistenciaTotal,
                    }
                    congreso_actualizado = CongresoJinisForm(contexto, instance=congreso)
                    if congreso_actualizado.is_valid():
                        congreso_actualizado.save()
                        editarDias(request, idcongreso, fechaInicio, fechaFin, pk)
                        messages.success(request, 'Congreso actualizado con éxito')
                    else:
                        messages.error(request, congreso_actualizado.errors)
                except MaeCongreso.DoesNotExist:
                    messages.error(request, 'El congreso ya no existe')
            return redirect(reverse('RegistrarCongreso', kwargs={'pk':pk}))
        else:
            administrador_congreso = AdministradorCongreso.objects.get(idadministrador=pk)
            congreso = MaeCongreso.objects.filter(pk=administrador_congreso.idcongreso.pk) 
            return render(request, 'pages/mostrarCongreso.html', {
                'current_page': 'registrar_congreso',
                'congresos':congreso,
                'pk':pk
            })

def desactivarDias(request, idcongreso, pk):
    try:
        dias = MaeDia.objects.filter(idcongreso=idcongreso)
        for i in range(0, len(dias)):
            dias[i].estado = 'NO ACTIVO'
            dias[i].save()
        messages.success(request, 'Dias del congreso desactivados con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception:
        messages.error(request, 'Error al desactivar los dias del congreso')
    return redirect(reverse('RegistrarCongreso', kwargs={'pk':pk}))

def activarDias(request, idcongreso, pk):
    try:
        dias = MaeDia.objects.filter(idcongreso=idcongreso)
        for i in range(0, len(dias)):
            dias[i].estado = 'ACTIVO'
            dias[i].save()
        messages.success(request, 'Dias del congreso activados con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception:
        messages.error(request, 'Error al activar los dias del congreso')
    return redirect(reverse('RegistrarCongreso', kwargs={'pk':pk}))

def editarDias(request, idcongreso, fechaInicio, fechaFin, pk):
    try:
        date_range = pd.date_range(start=fechaInicio, end=fechaFin) #Generación de rangos desde la fecha de inicio hasta la fecha fin
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        dias = MaeDia.objects.filter(idcongreso=idcongreso).order_by('pk')
        dias.delete()
        for i in range(0, len(date_list)):
            lista_dias = MaeDia(
                fecha = date_list[i],
                idcongreso = MaeCongreso.objects.get(pk=idcongreso)
            )
            lista_dias.save()
        messages.success(request, 'Se editaron los dias del congreso con éxito')
    except MaeDia.DoesNotExist:
        messages.error(request, 'No se encontró el día del congreso')
    except Exception as e:
        messages.error(request, e)
    return redirect(reverse('RegistrarCongreso', kwargs={'pk':pk}))
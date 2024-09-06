from django.urls import reverse
from django.views import View
from .decorators import colaborador_login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from Bloque.models import MaeBloque
from Asistencia.models import TrsAsistencia
from ParticipanteCongreso.models import ParticipanteCongreso
from datetime import date, datetime

class LoginColaborador(View):
    def get(self, request):
        error = request.session.pop('error', None)  # Obtiene y elimina el mensaje de error de la sesión
        return render(request, 'login/loginColaborador.html', {'error': error})
    
    def post(self, request):
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasenia')
        
        if not correo and not contrasenia:
            request.session['error'] = 'Por favor, ingrese sus credenciales'
            return redirect('LoginColaborador')

        try:
            colaborador = MaeColaborador.objects.get(correo=correo, contrasenia=contrasenia)
            request.session['codcolaborador'] = colaborador.pk
            return redirect(reverse('InterfazColaborador', kwargs={'pk': colaborador.pk}))
        except MaeColaborador.DoesNotExist:
            request.session['error'] = 'Credenciales incorrectas'
            return redirect('LoginColaborador')

class Colaborador(viewsets.ViewSet):
    @method_decorator(csrf_exempt)
    @method_decorator(colaborador_login_required)
    @action(detail=False, methods=['post', 'get'])
    def interfaz_colaborador(self, request, pk):
        if request.method == 'POST':
            try:
                data = request.data  # Usar request.data para obtener los datos JSON
                qr_data = json.loads(data.get('qr_code'))
                bloque_actual = json.loads(data.get('bloque'))
                required_fields = ['DNI', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRES', 'CORREO', 'CONGRESO']
                hora_actual = datetime.now().strftime("%H:%M")
                
                # Verificar que todos los campos necesarios están presentes
                if not all (field in qr_data for field in required_fields):
                    response_data = {
                        'status': 'error', 
                        'message': 'QR no válido'
                    }
                else:
                    participante = ParticipanteCongreso.objects.get(codparticipante=qr_data['DNI'], idcongreso=qr_data['CONGRESO'])
                    bloque_encontrado = MaeBloque.objects.get(idbloque=bloque_actual) #Corregir para que no se marque despues del bloque
                    bloqueColaborador = BloqueColaborador.objects.get(idcongreso=qr_data['CONGRESO'], idbloque=bloque_encontrado)

                    if not TrsAsistencia.objects.filter(idpc = participante, idbc = bloqueColaborador).exists():
                        if bloque_encontrado.horainicio.strftime("%H:%M") <= hora_actual and bloque_encontrado.horafin.strftime("%H:%M") >= hora_actual:
                            #Registro de asistencia
                            asistencia = TrsAsistencia(
                                idpc = participante,
                                idbc = bloqueColaborador,
                                idcongreso = participante.idcongreso
                            )
                            asistencia.save()
                            response_data = {
                                'status': 'success',
                                'message': 'Registro exitoso'
                            }
                        else:
                            response_data = {
                                'status': 'error', 
                                'message': 'El bloque no está abierto'
                            }
                    else:
                        response_data = {
                            'status': 'warning',
                            'message': 'El Registro ya existe'
                        }
                
                return JsonResponse(response_data)
            except MaeBloque.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'El bloque no existe'}, status=404)
            except BloqueColaborador.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'El bloque no está disponible'}, status=404)
            except ParticipanteCongreso.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'El participante no está registrado'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'QR no válido'}, status=400)
        else:
            colaborador = MaeColaborador.objects.get(pk=pk)
            colaborador_bloque = BloqueColaborador.objects.filter(idcolaborador=colaborador.idcolaborador)
            dia_actual = date.today().strftime('%d/%m/%Y') #Que aparesca segun el dia actual los bloques
            return render(request, 'asistencia_colaborador.html', {
                'pk': colaborador.pk,
                'colaborador': colaborador.nombres.capitalize() + ' ' + colaborador.apellidos.capitalize(), 
                'bloques': colaborador_bloque, 
                'congreso': colaborador_bloque.first(),
                'dia_actual': dia_actual,
            })
        
    @method_decorator(colaborador_login_required)
    def cerrar_sesion(self, request):
        request.session.flush()
        return redirect('LoginColaborador')
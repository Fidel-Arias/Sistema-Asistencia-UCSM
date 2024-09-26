from django.urls import reverse
from django.views import View
from .decorators import colaborador_login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from Bloque.models import MaeBloque
from Asistencia.models import TrsAsistencia
from ParticipanteCongreso.models import ParticipanteCongreso
from Participantes.models import MaeParticipantes
from tipoDocumento.models import MaeTipodocumento
from tipoParticipante.models import MaeTipoParticipante
from Ubicacion.models import MaeUbicacion
from datetime import date, datetime, timedelta
import qrcode
import os
from config import settings

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
                required_fields = ['DNI', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRES', 'CONGRESO']

                # Verificar que todos los campos necesarios están presentes
                if not all (field in qr_data for field in required_fields):
                    response_data = {
                        'status': 'error',
                        'message': 'QR no válido'
                    }
                else:
                    colaborador = MaeColaborador.objects.get(pk=pk)
                    participante = ParticipanteCongreso.objects.get(codparticipante=qr_data['DNI'], idcongreso=qr_data['CONGRESO'])
                    bloque_encontrado = MaeBloque.objects.get(idbloque=bloque_actual) #Corregir para que no se marque despues del bloque
                    bloqueColaborador = BloqueColaborador.objects.get(idcongreso=qr_data['CONGRESO'], idbloque=bloque_encontrado, idcolaborador=colaborador)

                    #MARCAR ASISTENCIA
                    response_data = marcar_Asistencia(participante, bloqueColaborador, bloque_encontrado)

                return JsonResponse(response_data)
            except MaeBloque.DoesNotExist:
                return JsonResponse({'title': 'Bloque no encontrado', 'status': 'error', 'message': 'El bloque no existe'}, status=404)
            except BloqueColaborador.DoesNotExist:
                return JsonResponse({'title': 'Bloque cerrado', 'status': 'error', 'message': 'El bloque no está disponible'}, status=404)
            except ParticipanteCongreso.DoesNotExist:
                return JsonResponse({'title': 'Usuario no encontrado', 'status': 'error', 'message': 'El usuario no está registrado'}, status=404)
            except Exception as e:
                print("Error3:", e)
                return JsonResponse({'title': 'Error', 'status': 'error', 'message': 'Ocurrió un error'}, status=500)
            except json.JSONDecodeError:
                return JsonResponse({'title': 'Error', 'status': 'error', 'message': 'QR no válido'}, status=400)
        else:
            colaborador = MaeColaborador.objects.get(pk=pk)
            colaborador_bloque = BloqueColaborador.objects.filter(idcolaborador=colaborador.idcolaborador)
            dia_actual = date.today().strftime('%d/%m/%Y') #Que aparesca segun el dia actual los bloques
            hora_actual = datetime.now().strftime("%H:%M")
            bloque_selected = None
            ubicacion = 'Desconocido'

            for bloque in colaborador_bloque:
                minuto_inicial = bloque.idbloque.horainicio.minute
                hora_inicial = bloque.idbloque.horainicio.hour

                if (calcular_diferencia_minutos_bloque_inicial(hora_inicial, minuto_inicial).strftime('%H:%M') <= hora_actual and bloque.idbloque.horafin.strftime('%H:%M') >= hora_actual):
                    bloque_selected = bloque.idbloque
                    ubicacion = bloque.idbloque.idubicacion
                    break

            return render(request, 'asistencia_colaborador.html', {
                'pk': colaborador.pk,
                'colaborador': colaborador.nombres.title() + ' ' + colaborador.apellidos.title(),
                'bloques': colaborador_bloque,
                'congreso': colaborador_bloque.first(),
                'dia_actual': dia_actual,
                'bloque_selected': bloque_selected,
                'ubicacion': ubicacion,
            })

    @method_decorator(colaborador_login_required)
    def cerrar_sesion(self, request):
        request.session.flush()
        return redirect('LoginColaborador')

    @method_decorator(colaborador_login_required)
    @action(detail=False, methods=['post'])
    def registrar_participante_no_figurado(self, request, pk):
        if request.method == 'POST':
            try:
                data = request.data
                dni = data['dni']
                nombres = data['nombres'].upper()
                ap_materno = data['ap_materno'].upper()
                ap_paterno = data['ap_paterno'].upper()
                bloque_actual = data['bloque']

                #Verificar que no exista en el registro
                if not MaeParticipantes.objects.filter(pk=dni).exists():
                    with transaction.atomic():
                        participante_no_registrado = MaeParticipantes(
                            codparticipante=dni,
                            nombre = nombres,
                            ap_paterno = ap_paterno,
                            ap_materno = ap_materno,
                            idtipodoc = MaeTipodocumento.objects.get(pk='1'),
                            idtipo = MaeTipoParticipante.objects.get(pk='1'),
                            estado = 'NO REGISTRADO',
                        )
                        participante_no_registrado.save()
                        participante_congreso = ParticipanteCongreso(
                            codparticipante=participante_no_registrado,
                            idcongreso = BloqueColaborador.objects.filter(idcolaborador=pk).first().idcongreso
                        )
                        participante_congreso.save()
                        generar_qr_code(participante_congreso)
                        colaborador = MaeColaborador.objects.get(pk=pk)
                        bloque_encontrado = MaeBloque.objects.get(idbloque=bloque_actual)
                        bloqueColaborador = BloqueColaborador.objects.get(idcongreso=participante_congreso.
                        idcongreso.idcongreso, idbloque=bloque_encontrado, idcolaborador=colaborador)

                        response_data = marcar_Asistencia(participante_congreso, bloqueColaborador, bloque_encontrado)
                else:
                    response_data = {
                        'title': 'Usuario existente',
                       'status': 'error',
                       'message': 'El usuario ya existe'
                    }
                return JsonResponse(response_data)
            except Exception as e:
                print('Error 2: ', e)
                return JsonResponse({'title': 'Error', 'status': 'error', 'message': 'Ocurrió un error'}, status=500)

    @method_decorator(colaborador_login_required)
    @action(detail=False, methods=['post'])
    def registrar_participante_por_teclado(self, request, pk):
        try:
            data = request.data
            dni = data['dni']
            bloque = data['bloque']

            participante = MaeParticipantes.objects.get(pk=dni) #Busca al participante
            colaborador = MaeColaborador.objects.get(pk=pk)
            participante_congreso = ParticipanteCongreso.objects.get(codparticipante=participante)
            bloque_actual = MaeBloque.objects.get(pk=bloque) #Busca el bloque seleccionado
            bloqueColaborador = BloqueColaborador.objects.get(idcongreso=participante_congreso.idcongreso.idcongreso, idbloque=bloque_actual, idcolaborador=colaborador)

            #Registrar Asistencia
            response_data = marcar_Asistencia(participante_congreso, bloqueColaborador, bloque_actual)
            return JsonResponse(response_data, status=200)
        except Exception as e:
            print('Error: ', e)
            return JsonResponse({'title':'Error', 'status': 'error','message': 'DNI no válido'}, status=400)
        except MaeParticipantes.DoesNotExist:
            return JsonResponse({'title': 'Usuario no encontrado', 'status': 'error', 'message': 'El usuario no está registrado'}, status=404)
        except MaeBloque.DoesNotExist:
            return JsonResponse({'title': 'Bloque no encontrado', 'status': 'error','message': 'El bloque no existe'}, status=404)

def generar_qr_code(participante_congreso):
    participante = participante_congreso.codparticipante
    data = {
        'DNI': participante.pk,
        'AP_PATERNO': participante.ap_paterno,
        'AP_MATERNO': participante.ap_materno,
        'NOMBRES': participante.nombre,
        'CONGRESO': participante_congreso.idcongreso.idcongreso
    }
    json_data = json.dumps(data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    # Nombre y path del archivo
    file_name = f"{participante.pk}.png"
    file_path = os.path.join(settings.BASE_DIR, 'static/qrcodes', file_name)
    # file_path = f'static/qrcodes/{file_name}'

    # Guardar imagen en la carpeta qrcodes
    img.save(file_path)

    # Guardar la URL relativa del archivo en la base de datos
    file_url = f"{settings.STATIC_URL}qrcodes/{file_name}"
    participante.qr_code = file_url
    participante.save()

def marcar_Asistencia(participante, bloqueColaborador, bloque_encontrado):
    #Hora y minuto Inicial
    hora_actual = datetime.now().strftime("%H:%M") #Hora actual
    minuto_inicial = bloque_encontrado.horainicio.minute
    hora_inicial = bloque_encontrado.horainicio.hour
    #Hora y minuto final
    minuto_final = bloque_encontrado.horafin.minute
    hora_final = bloque_encontrado.horafin.hour
    if not TrsAsistencia.objects.filter(idpc = participante, idbc__idbloque = bloqueColaborador.idbloque.pk).exists():
        if (calcular_diferencia_minutos_bloque_inicial(hora_inicial, minuto_inicial)).strftime("%H:%M") <= hora_actual and calcular_diferencia_minutos_bloque_final(hora_final, minuto_final).strftime("%H:%M") >= hora_actual:
            #Registro de asistencia
            asistencia = TrsAsistencia(
                idpc = participante,
                idbc = bloqueColaborador,
                idcongreso = participante.idcongreso
            )
            asistencia.save()
            response_data = {
                'title': 'Asistencia marcada',
                'status': 'success',
                'message': 'Registro exitoso'
            }
        else:
            response_data = {
                'title': 'Bloque Cerrado',
                'status': 'error',
                'message': 'El bloque no está abierto'
            }

    else:
        response_data = {
            'title': 'Usuario registrado',
            'status': 'warning',
            'message': 'El Registro ya existe'
        }
    return response_data

def calcular_diferencia_minutos_bloque_inicial(hora, minuto):
    tiempo_inicial = datetime.combine(datetime.today(), datetime.min.time()).replace(hour=hora, minute=minuto)
    nueva_hora = tiempo_inicial - timedelta(minutes=15)
    return nueva_hora

def calcular_diferencia_minutos_bloque_final(hora, minuto):
    tiempo_final = datetime.combine(datetime.today(), datetime.min.time()).replace(hour=hora, minute=minuto)
    nueva_hora = tiempo_final + timedelta(minutes=15)
    return nueva_hora
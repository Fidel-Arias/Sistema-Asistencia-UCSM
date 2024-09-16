from ..decorators import administrador_login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from Congreso.models import MaeCongreso
from adminMaestros.models import AdministradorCongreso
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from Participantes.models import MaeParticipantes
from tipoDocumento.models import MaeTipodocumento
from tipoParticipante.models import MaeTipoParticipante
from ParticipanteCongreso.models import ParticipanteCongreso
from django.db import transaction
from django.contrib import messages
import qrcode
import json
import pandas as pd
from config import settings
import os

#Variables locales
archivo_subido = False

class Importar_Datos(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def importar_datos(self, request, pk):
        global archivo_subido
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            admin_congreso = AdministradorCongreso.objects.get(idadministrador = pk)

            #Procesando el archivo
            try:
                if filename.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    messages.error(request, 'Formato de archivo no soportado')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {e}')

            try:
                datos_participante = []
                for index, row in df.iterrows():
                    datos_participante.append({
                        'DNI': row['DNI'],
                        'AP_PATERNO': row['Ap. Paterno'],
                        'AP_MATERNO': row['Ap. Materno'],
                        'NOMBRES': row['Nombres'],
                        'CORREO': row['Correo'],
                        'TIPO': row['Tipo'].upper(),
                    })

                for dato in datos_participante:
                    if not MaeParticipantes.objects.filter(pk=dato['DNI']).exists(): #SI EXISTE SOLO ACTUALIZAR SUS DATOS
                        with transaction.atomic():
                            agregando_participantes = MaeParticipantes(
                                codparticipante=dato['DNI'],
                                ap_paterno=dato['AP_PATERNO'],
                                ap_materno=dato['AP_MATERNO'],
                                nombre=dato['NOMBRES'],
                                correo=dato['CORREO'],
                                idtipodoc=MaeTipodocumento.objects.get(pk=1),
                                idtipo=MaeTipoParticipante.objects.get(dstipo=dato['TIPO']),
                                estado='REGISTRADO'
                            )
                            agregando_participantes.save()
                archivo_subido = True
                fs.delete(filename)

                #Asociando a la tabla ParticipanteCongreso
                participantes = MaeParticipantes.objects.all()
                with transaction.atomic():
                    for participante in participantes:
                        if not ParticipanteCongreso.objects.filter(codparticipante=participante.pk).exists():
                            ParticipanteCongreso.objects.create(
                                codparticipante=MaeParticipantes.objects.get(pk=participante.pk),
                                idcongreso=admin_congreso.idcongreso
                            )

                messages.success(request, 'Archivo importado y procesado con éxito')
                return redirect(reverse('ImportarDatos', kwargs={'pk':pk}))

            except Exception:
                archivo_subido = False
                messages.error(request, 'Error en las columnas del archivo')
                return redirect(reverse('ImportarDatos', kwargs={'pk':pk}))

        else:
            return render(request, 'pages/importarDatos.html', {
                'current_page': 'importar_datos',
                'archivo_subido': archivo_subido,
                'pk': pk
            })

class Generar_QRCode(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def generar_codigo_qrcode(self, request, pk):
        global archivo_subido
        if request.method == 'POST':
            try:
                participantes_congreso = ParticipanteCongreso.objects.all()
                data = {}
                for participante_congreso in participantes_congreso:
                    participante = participante_congreso.codparticipante
                    congreso = participante_congreso.idcongreso
                    data = {
                        'DNI': participante.codparticipante,
                        'AP_PATERNO': participante.ap_paterno,
                        'AP_MATERNO': participante.ap_materno,
                        'NOMBRES': participante.nombre,
                        'CORREO': participante.correo,
                        'CONGRESO': congreso.idcongreso
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

                messages.success(request, 'Códigos QR generado con éxito')
                archivo_subido = False

                return render(request, 'pages/importarDatos.html', {
                'current_page': 'importar_datos',
                'archivo_subido': archivo_subido,
                'pk': pk
            })
            except Exception:
                messages.error(request, 'Error al generar los códigos QR')
                archivo_subido = False
                return redirect(reverse('ImportarDatos', kwargs={'pk': pk}))
        else:
            return redirect('ImportarDatos')

def enviar_email_participantes(datos_user, img_path):
    try:
        template = render_to_string('messages/mail_colaborador.html', {

        })
    except Exception:
        return 'failed'

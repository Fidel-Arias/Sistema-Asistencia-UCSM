from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from Asistencia.models import TrsAsistencia
from adminMaestros.models import AdministradorCongreso
import pandas as pd

class ReporteAsistencia(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def generar_reporte(self, request, pk):
        if request.method == 'POST':
            try:
                nombre_archivo = request.POST.get('input-name')
                administrador = AdministradorCongreso.objects.get(idadministrador=pk)
                listaAsistencia = TrsAsistencia.objects.filter(idcongreso=administrador.idcongreso)
                data = []
                dni_procesados = set() #Procesa datos no repetidos
                for asistencia in listaAsistencia:
                    dni = asistencia.idpc.codparticipante.codparticipante
                    if dni not in dni_procesados:
                        cantidad_asistencia = TrsAsistencia.objects.filter(
                            idpc=asistencia.idpc
                        ).count()
                        data.append({
                            'DNI': dni,
                            'NOMBRES': asistencia.idpc.codparticipante.nombre,
                            'AP_MATERNO': asistencia.idpc.codparticipante.ap_materno,
                            'AP_PATERNO': asistencia.idpc.codparticipante.ap_paterno,
                            'CONGRESO': asistencia.idbc.idcongreso.nombre,
                            'TIPO': asistencia.idpc.codparticipante.idtipo,
                            'CANTIDAD DE ASISTENCIA': cantidad_asistencia
                        })
                        dni_procesados.add(dni)
                dataframe = pd.DataFrame(data)

                # Crear un objeto HttpResponse con el tipo de contenido de Excel
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={nombre_archivo}.xlsx'
                
                # Usar XlsxWriter como motor de pandas ExcelWriter
                with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
                    dataframe.to_excel(writer, index=False, sheet_name='Asistencia')

                return response
            except Exception as e:
                return HttpResponse(str(e))
        else:
            admin = AdministradorCongreso.objects.get(idadministrador=pk)
            is_there_Data = True if TrsAsistencia.objects.filter().exists() else False
            return render(request, 'pages/generarReporte.html', {
                'current_page':'generar_reportes',
                'pk':admin.idadministrador.idadministrador,
                'is_there_Data': is_there_Data
            })
    
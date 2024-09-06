from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from Asistencia.models import TrsAsistencia
from Admin.models import MaeAdministrador
import pandas as pd

class ReporteAsistencia(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def generar_reporte(self, request, pk):
        if request.method == 'POST':
            nombre_archivo = request.POST.get('input-name')
            administrador = MaeAdministrador.objects.get(pk=pk)
            listaAsistencia = TrsAsistencia.objects.filter(idcongreso=administrador.idcongreso).order_by('pk')
            data = []
            for asistencia in listaAsistencia:
                cantidad_asistencia = TrsAsistencia.objects.filter(
                    idpc=asistencia.idpc
                ).count()
                data.append({
                    'DNI': asistencia.idpc.codparticipante.codparticipante,
                    'NOMBRES': asistencia.idpc.codparticipante.nombre,
                    'AP_MATERNO': asistencia.idpc.codparticipante.ap_materno,
                    'AP_PATERNO': asistencia.idpc.codparticipante.ap_paterno,
                    'CONGRESO': asistencia.idbc.idcongreso.nombre,
                    'TIPO': asistencia.idpc.codparticipante.idtipo,
                    'CANTIDAD DE ASISTENCIA': cantidad_asistencia
                })
            dataframe = pd.DataFrame(data)

            # Crear un objeto HttpResponse con el tipo de contenido de Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={nombre_archivo}.xlsx'
            
            # Usar XlsxWriter como motor de pandas ExcelWriter
            with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Asistencia')

            return response
        else:
            admin = MaeAdministrador.objects.get(pk=pk)
            is_there_Data = True if TrsAsistencia.objects.filter().exists() else False
            return render(request, 'pages/generarReporte.html', {
                'current_page':'generar_reportes',
                'pk':admin.pk,
                'is_there_Data': is_there_Data
            })
    
from .models import MaeCongreso
import pandas as pd
from Dia.models import MaeDia
from Congreso.models import MaeCongreso
from django.db import transaction, DatabaseError
from django.http import HttpResponse
from rest_framework import status

def creando_nuevo_congreso(formulario):
    #Validar q no se repia congreso y agregar la tabla admin congreso y quitar las opcones select
    try:
        nombre = formulario['nombreCongreso']
        asistencias = formulario['asistencia']
        fecha_inicio = formulario['fechaInicioCongreso']
        fecha_fin = formulario['fechaFinCongreso']

        with transaction.atomic():
            if (not(MaeCongreso.objects.filter(nombre=nombre).exists())):
                nuevo_congreso = MaeCongreso(
                    nombre=nombre,
                    asistenciatotal=asistencias,
                    fechainicio=fecha_inicio,
                    fechafin=fecha_fin
                )

                nuevo_congreso.save()
                is_valid = generacion_ingreso_tabla_dias(fecha_inicio, fecha_fin, nuevo_congreso.pk)
                if is_valid == 'failed':
                    return HttpResponse("""
                        <html>
                            <body>
                                <p>Error al generar los días del congreso</p>
                            </body>
                        </html>
                    """, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return 'exists'
        return 'success'
    except Exception:
        return 'failed'
    
def generacion_ingreso_tabla_dias(fechaInicio, fechaFin, idcongreso):
    try:
        date_range = pd.date_range(start=fechaInicio, end=fechaFin) #Generación de rangos desde la fecha de inicio hasta la fecha fin
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        lista_dias = None
        with transaction.atomic():
            for i in range(0, len(date_list)):
                lista_dias = MaeDia(
                    fecha = date_list[i],
                    idcongreso = MaeCongreso.objects.get(pk=idcongreso)
                )
                lista_dias.save()
        return 'success'
    except DatabaseError:
        return 'failed'
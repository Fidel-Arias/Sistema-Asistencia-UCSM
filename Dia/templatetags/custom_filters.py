'''Crear el Filtro Personalizado:
En Django, los filtros personalizados se definen dentro de un archivo Python en el directorio templatetags

En este filtro, format_fecha toma la fecha en formato YYYY-MM-DD, la divide en partes para obtener el año, el mes y el día, y luego aplica la función meses para obtener el nombre del mes en

Después de definir el filtro, asegúrate de cargarlo en tu template donde quieres formatear la fecha. Para cargar los filtros personalizados

Luego, donde quieras mostrar la fecha formateada:

<td>{{ participante.fecha|format_fecha }}</td>

'''

from django import template
from Dia.models import meses  # importar la función meses de tu models.py

register = template.Library()

@register.filter(name='format_fecha')
def format_fecha(value):
    # value es la fecha en formato ISO 8601 (YYYY-MM-DD)
    parts = value.split('-')
    year = parts[0]
    month = int(parts[1])
    day = parts[2]

    return f'{day} de {meses(month)} de {year}'

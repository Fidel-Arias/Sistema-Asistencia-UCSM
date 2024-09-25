from django.urls import path
from .admin import Cerrar_Sesion
from .views import colaboradores, congreso, ponentes, bloques, ponencias, ubicacion, bloquesColaborador, reporte, importar, interfaz, registrar_asistencia

urlpatterns = [
    path('bienvenido/<int:pk>/', interfaz.Interfaz_Administrador.as_view({'get':'interfaz_administrador'}), name='InterfazAdministrador'),
    path('generar_reporte/<int:pk>/', reporte.ReporteAsistencia.as_view({'get':'generar_reporte', 'post':'generar_reporte'}), name='GenerarReporte'),
    path('registrar_colaboradores/<int:pk>/', colaboradores.Registrar_Colaboradores.as_view({'get':'registrar_colaboradores', 'post':'registrar_colaboradores'}), name='RegistrarColaboradores'),
    path('registrar_ponencias/<int:pk>/', ponencias.Registrar_Ponencias.as_view({'get':'registrar_ponencias', 'post':'registrar_ponencias'}), name='RegistrarPonencia'),
    path('registrar_ponentes/<int:pk>/', ponentes.Registrar_Ponentes.as_view({'get':'registrar_ponentes', 'post':'registrar_ponentes'}), name='RegistrarPonentes'),
    path('registrar_congreso/<int:pk>/', congreso.Registrar_Congreso.as_view({'get':'registrar_congreso', 'post':'registrar_congreso'}), name='RegistrarCongreso'),
    path('registrar_ubicacion/<int:pk>/', ubicacion.Registrar_Ubicacion.as_view({'get':'registrar_ubicacion', 'post':'registrar_ubicacion'}), name='RegistrarUbicaciones'),
    path('registrar_bloques/<int:pk>/', bloques.Registrar_Bloques.as_view({'get':'registrar_bloques', 'post':'registrar_bloques'}), name='RegistrarBloques'),
    path('registrar_bloques_colaboradores/<int:pk>/', bloquesColaborador.Registrar_Bloques_Colaborador.as_view({'get':'registrar_bloques_colaboradores', 'post':'registrar_bloques_colaboradores'}), name='RegistrarBloqueColaborador'),
    path('importar_datos/<int:pk>/', importar.Importar_Datos.as_view({'get':'importar_datos', 'post':'importar_datos'}), name='ImportarDatos'),
    path('generar_qrcode/<int:pk>/', importar.Generar_QRCode.as_view({'get':'generar_codigo_qrcode', 'post':'generar_codigo_qrcode'}), name='GenerarQRCode'),
    path('', Cerrar_Sesion.as_view({'get':'cerrar_sesion'}), name='CerrarSesion'),
    path('registrar_asistencia/<int:pk>/', registrar_asistencia.Registrar_Asistencia_por_Fallas.as_view({'get':'registrar_asistencia', 'post':'registrar_asistencia'}), name='RegistrarAsistencia'),
]
from django.urls import path
from .views import Colaborador

urlpatterns = [
    path('dashboard/<int:pk>', Colaborador.as_view({'get':'interfaz_colaborador', 'post': 'interfaz_colaborador'}), name='InterfazColaborador'),
    path('cerrar_sesion/', Colaborador.as_view({'get':'cerrar_sesion'}), name='SalirColaborador'),
    path('registro_para_no_figurados/<int:pk>', Colaborador.as_view({'post':'registrar_participante_no_figurado'}), name='RegistroNoFigurado'),
    path('registro_manual_para_figurados/<int:pk>', Colaborador.as_view({'post':'registrar_participante_por_teclado'}), name='RegistroManualParticipante')
]
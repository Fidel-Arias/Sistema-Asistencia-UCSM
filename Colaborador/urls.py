from django.urls import path
from .views import Colaborador

urlpatterns = [
    path('dashboard/<int:pk>', Colaborador.as_view({'get':'interfaz_colaborador', 'post': 'interfaz_colaborador'}), name='InterfazColaborador'),
    path('cerrar_sesion/', Colaborador.as_view({'get':'cerrar_sesion'}), name='SalirColaborador')
]
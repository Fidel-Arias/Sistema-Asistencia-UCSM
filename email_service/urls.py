from django.urls import path
from .token import activar_admin

urlpatterns = [
    path('', activar_admin, name='activar_admin'),
]
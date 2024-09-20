"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Participantes.views import LoginView
from Colaborador.views import LoginColaborador
from Admin.admin import LoginAdmin, RegisterAdmin
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True)),
    path('accounts/login/', LoginView.as_view(), name='Login'),  # URL para la vista de inicio de sesión personalizada
    path('accounts/administrador/login-admin/', LoginAdmin.as_view(), name='LoginAdmin'),  # URL para la vista de inicio de sesión personalizada
    path('accounts/administrador/register-admin/', RegisterAdmin.as_view(), name='RegisterAdmin'),
    path('accounts/colaborador/login-colaborador/', LoginColaborador.as_view(), name='LoginColaborador'),  # URL para la vista de inicio de sesión personalizada
    path('dashboard/', include('Participantes.urls')),  # Incluye las URLs de la aplicación Participantes    
    path('administrador/dashboard/', include('Admin.urls')),
    path('colaborador/', include('Colaborador.urls')),
    path('verificar_admin/', include('email_service.urls')),
]

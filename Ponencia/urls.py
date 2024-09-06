from django.urls import path
from .views import viewPonencias

urlpatterns = [
    path('<int:pk>/ponencias/', viewPonencias.as_view({'get':'verPonencias'}), name="Ponencias"),
]
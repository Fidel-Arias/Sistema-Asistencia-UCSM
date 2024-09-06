from rest_framework import serializers
from .models import MaePonencia

class PonenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaePonencia
        fields = ('idponencia', 'idponente', 'nombre')
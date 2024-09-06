from rest_framework import serializers
from .models import MaeAdministrador, AdminToken

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaeAdministrador
        fields = ('nombres', 'apellidos', 'correo', 'contrasenia', 'idtipo')

    def create(self, validated_data):
        return MaeAdministrador.objects.create(**validated_data)
    
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminToken
        fields = ('token','admin')
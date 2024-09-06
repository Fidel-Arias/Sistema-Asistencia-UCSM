from rest_framework import serializers
from .models import MaeDia

class DiaSerializer(serializers.ModelSerializer):
    iddia = serializers.StringRelatedField() #Al usar StringRelatedField() para iddia, se  indica a Django REST Framework que debe usar el método __str__() de MaeDia para representar este campo.
    class Meta:
        model = MaeDia
        fields = ['iddia', 'fecha']
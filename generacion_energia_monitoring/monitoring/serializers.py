# monitoring/serializers.py
from rest_framework import serializers
from .models import TipoDispositivo, StatusDispositivo, Dispositivo, Lectura, Mantenimiento

class TipoDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDispositivo
        fields = '__all__'
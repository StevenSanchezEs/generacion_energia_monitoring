# monitoring/serializers.py
from rest_framework import serializers
from .models import TipoDispositivo, StatusDispositivo, Dispositivo, Lectura, Mantenimiento

class TipoDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDispositivo
        fields = '__all__'

class StatusDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusDispositivo
        fields = '__all__'
        
class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'

class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = '__all__'
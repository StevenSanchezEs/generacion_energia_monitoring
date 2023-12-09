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
    
    def validate(self, data):
        # Verifica si la clave 'dispositivo' está presente en data
        dispositivo = data.get('dispositivo')

        if dispositivo:
            # Verifica si el dispositivo está en mantenimiento
            if dispositivo.status_dispositivo.descripcion == "En mantenimiento":
                raise serializers.ValidationError("No se puede realizar este registro ya que el dispositivo se encuentra en mantenimiento")

        # Verifica si la potencia es negativa
        if data.get('potencia_actual', 0) < 0:
            raise serializers.ValidationError("El valor de la potencia no debe ser negativo")

        return data
    
class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
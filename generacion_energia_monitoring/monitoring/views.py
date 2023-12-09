from rest_framework.decorators import action
from datetime import datetime
from rest_framework.decorators import authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from .models import TipoDispositivo, StatusDispositivo, Dispositivo, Lectura, Mantenimiento
from .serializers import TipoDispositivoSerializer, StatusDispositivoSerializer, DispositivoSerializer, LecturaSerializer, MantenimientoSerializer

# Create your views here.

class TipoDispositivoViewSet(viewsets.ModelViewSet):
    queryset = TipoDispositivo.objects.all()
    serializer_class = TipoDispositivoSerializer
    
class StatusDispositivoViewSet(viewsets.ModelViewSet):
    queryset = StatusDispositivo.objects.all()
    serializer_class = StatusDispositivoSerializer
    
class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Obtiene el estado del dispositivo antes de la actualización
        old_status = instance.status_dispositivo

        # Actualiza el dispositivo
        self.perform_update(serializer)

        # Verifica si el estado del dispositivo ha cambiado a "En mantenimiento"
        if instance.status_dispositivo != old_status and instance.status_dispositivo.descripcion == "En mantenimiento":
            # Crea un registro de mantenimiento
            mantenimiento = Mantenimiento.objects.create(dispositivo=instance)

            # Obtén todos los registros de mantenimiento asociados al dispositivo actual
            registros_mantenimiento = Mantenimiento.objects.filter(dispositivo=instance)

            # Serializa los registros de mantenimiento
            serializer_mantenimiento = MantenimientoSerializer(registros_mantenimiento, many=True)

            # Devuelve la respuesta con los registros de mantenimiento
            return Response({
                "dispositivo": serializer.data,
                "registros_mantenimiento": serializer_mantenimiento.data
            })

        return Response(serializer.data)
    
    
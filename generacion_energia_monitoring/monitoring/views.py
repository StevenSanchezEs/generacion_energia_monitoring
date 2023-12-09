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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('tipo_dispositivo', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Id del tipo de dispositivo por ejemplo: "id": 1, "nombre": aerogenerador'),
        ],
        responses={200: openapi.Response(
                description="Ok",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "nombre": "Generador CDMX",
                            "fecha_alta": "2023-12-08T16:32:25.358812-06:00",
                            "fecha_actualizacion": "2023-12-09T02:23:25.474365-06:00",
                            "potencia_actual": 20.0,
                            "tipo_dispositivo": 1,
                            "status_dispositivo": 2
                        }
                    ]
                }
            ), 400: 'Parámetros inválidos'},
        #operation_id='obtener_lecturas_por_tipo',
        operation_description='Obtiene todos los dispositivos que coincidan con el id que se pasa por parametro, por ejemplo: con un id = 1 se obtienen todos los del tipo aerogenerador.',
    )
    
    @action(detail=False, methods=['GET'])
    def obtener_por_tipodispositivo(self, request, *args, **kwargs):
        # Implementa la lógica para obtener dispositivos por tipo de dispositivo
        tipo_dispositivo_id = self.request.query_params.get('tipo_dispositivo', None)
        dispositivos = Dispositivo.objects.filter(tipo_dispositivo__id=tipo_dispositivo_id)
        serializer = DispositivoSerializer(dispositivos, many=True)
        return Response(serializer.data)
    
@authentication_classes([])  # Anula las clases de autenticación
@permission_classes([])  # Anula las clases de permisos
class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer
    
    def perform_create(self, serializer):
        # Obtiene el dispositivo asociado a la lectura
        dispositivo = serializer.validated_data['dispositivo']

        # Actualiza la potencia y la fecha de actualización del dispositivo
        dispositivo.potencia_actual = serializer.validated_data['potencia_actual']
        dispositivo.timestamp = serializer.validated_data.get('timestamp')  # Ajusta aquí

        # Guarda el dispositivo
        dispositivo.save()

        # Llama al método create del serializador para guardar la lectura
        serializer.save()

        return Response(serializer.data)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('tipo_dispositivo', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Id del tipo de dispositivo por ejemplo: "id": 3, "nombre": turbina hidroeléctrica'),
        ],
        responses={200: openapi.Response(
                description="Ok",
                examples={
                        "application/json": [
                            {
                                "id": 3,
                                "potencia_actual": 10.0,
                                "timestamp": "2023-12-08T18:09:51.235659-06:00",
                                "dispositivo": 2
                            }
                            ,
                            {
                                "id": 12,
                                "potencia_actual": 10.0,
                                "timestamp": "2023-12-09T01:56:14.153269-06:00",
                                "dispositivo": 2
                            }
                        ]
                    }
            ), 400: 'Parámetros inválidos'},
        #operation_id='obtener_lecturas_por_tipo',
        operation_description='Obtiene todos las lecturas por tipo de dispositivo.',
    )
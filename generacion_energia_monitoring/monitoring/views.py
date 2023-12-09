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
    
    @action(detail=False, methods=['GET'])
    def obtener_por_tipo_dispositivo(self, request, *args, **kwargs):
        tipo_dispositivo_id = self.request.query_params.get('tipo_dispositivo', None)

        # Filtra las lecturas por tipo de dispositivo
        lecturas = Lectura.objects.filter(dispositivo__tipo_dispositivo__id=tipo_dispositivo_id)

        serializer = LecturaSerializer(lecturas, many=True)
    
        return Response(serializer.data)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fecha_inicio', in_=openapi.IN_QUERY, type=openapi.TYPE_OBJECT, description='Fecha de inicio en formato YYYY-MM-DDTHH:MM:SS.SSSZ'),
            openapi.Parameter('fecha_fin', in_=openapi.IN_QUERY, type=openapi.TYPE_OBJECT, description='Fecha de fin en formato YYYY-MM-DDTHH:MM:SS.SSSZ'),
        ],
        responses={200: openapi.Response(
                description="Ok",
                examples={
                    "application/json": {
                    "energiaTotal": [
                        {
                            "idDispositivo": 1,
                            "Energia": 140.0
                        },
                        {
                            "idDispositivo": 2,
                            "Energia": 10.0
                        }
                    ]
                }
                }
            ), 400: 'Parámetros inválidos'},
        #operation_id='obtener_lecturas_por_tipo',
        operation_description='Obtiene la suma de todas las lecturas por cada dispositivo conforme al rango de fechas.',
    )
    
    @action(detail=False, methods=['get'])
    def obtener_energia_total(self, request):
        # Obtener parámetros de consulta
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        # Convertir cadenas de fecha a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%dT%H:%M:%S.%fZ") if fecha_inicio_str else None
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%dT%H:%M:%S.%fZ") if fecha_fin_str else None

        # Filtrar lecturas por rango de tiempo
        lecturas_filtradas = Lectura.objects.all()
        if fecha_inicio:
            lecturas_filtradas = lecturas_filtradas.filter(timestamp__gte=fecha_inicio)
        if fecha_fin:
            lecturas_filtradas = lecturas_filtradas.filter(timestamp__lte=fecha_fin)

        # Calcular la suma de potencia_actual agrupada por dispositivo
        resultado = lecturas_filtradas.values('dispositivo').annotate(energia_total=Sum('potencia_actual'))

        # Formatear el resultado como se solicitó
        respuesta = [{'idDispositivo': item['dispositivo'], 'Energia': item['energia_total']} for item in resultado]

        return Response({'energiaTotal': respuesta})
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('dispositivo', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Id del dispositivo por ejemplo: 1'),
        ],
        responses={200: openapi.Response(
                description="Ok",
                examples={
                        "application/json": [
                            {
                                "id": 1,
                                "potencia_actual": 30.0,
                                "timestamp": "2023-12-08T16:33:45.528435-06:00",
                                "dispositivo": 1
                            },
                            {
                                "id": 2,
                                "potencia_actual": 40.0,
                                "timestamp": "2023-12-08T17:04:55.762953-06:00",
                                "dispositivo": 1
                            },
                            {
                                "id": 4,
                                "potencia_actual": 30.0,
                                "timestamp": "2023-12-08T22:09:02.881799-06:00",
                                "dispositivo": 1
                            },
                            {
                                "id": 9,
                                "potencia_actual": 10.0,
                                "timestamp": "2023-12-08T23:21:12.043548-06:00",
                                "dispositivo": 1
                            },
                            {
                                "id": 10,
                                "potencia_actual": 20.0,
                                "timestamp": "2023-12-08T23:27:13.317827-06:00",
                                "dispositivo": 1
                            },
                            {
                                "id": 11,
                                "potencia_actual": 10.0,
                                "timestamp": "2023-12-08T23:39:21.296333-06:00",
                                "dispositivo": 1
                            }
                        ]
                    }
            ), 400: 'Parámetros inválidos'},
        #operation_id='obtener_lecturas_por_tipo',
        operation_description='Obtiene todos las lecturas relacionadas con el id del dispositivo.',
    )
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
    

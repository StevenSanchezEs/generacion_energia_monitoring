# monitoring/urls.py
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from .views import TipoDispositivoViewSet, StatusDispositivoViewSet, DispositivoViewSet, LecturaViewSet, MantenimientoViewSet

# Crea un enrutador y registra los viewsets
router = DefaultRouter()
router.register(r'tipo_dispositivo', TipoDispositivoViewSet, basename='tipo_dispositivo')
router.register(r'status_dispositivo', StatusDispositivoViewSet, basename='status_dispositivo')
router.register(r'dispositivos', DispositivoViewSet, basename='dispositivo')
router.register(r'lecturas', LecturaViewSet, basename='lectura')
router.register(r'mantenimientos', MantenimientoViewSet, basename='mantenimiento')

# Define las rutas adicionales
dispositivo_extra_routes = [
    path('obtener_por_tipo_dispositivo/', LecturaViewSet.as_view({'get': 'obtener_por_tipo_dispositivo'}), name='obtener_por_tipo_dispositivo'),
    path('obtener_por_id_dispositivo/', LecturaViewSet.as_view({'get': 'obtener_por_id_dispositivo'}), name='obtener_por_id_dispositivo'),
    path('lecturas/obtener_energia_total/', LecturaViewSet.as_view({'get': 'obtener_energia_total'}), name='obtener_energia_total'),
]
urlpatterns = [
    path('', include(router.urls)),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    *dispositivo_extra_routes,
]
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import IsAdminOrReadOnly
from api.models import (
    Rol, CatalogoEspecialidad, CatalogoDiagnostico, CatalogoObjetivo,
    CatalogoEstadoCaballo, CatalogoEventoEquino, CatalogoEstadoSesion,
    CatalogoEstadoPago, CatalogoParentesco
)
from api.serializers import (
    RolSerializer, CatalogoEspecialidadSerializer, CatalogoDiagnosticoSerializer,
    CatalogoObjetivoSerializer, CatalogoEstadoCaballoSerializer,
    CatalogoEventoEquinoSerializer, CatalogoEstadoSesionSerializer,
    CatalogoEstadoPagoSerializer, CatalogoParentescoSerializer
)

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEspecialidad.objects.all()
    serializer_class = CatalogoEspecialidadSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoDiagnostico.objects.all()
    serializer_class = CatalogoDiagnosticoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoObjetivoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoObjetivo.objects.all()
    serializer_class = CatalogoObjetivoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoCaballoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoCaballo.objects.all()
    serializer_class = CatalogoEstadoCaballoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEventoEquinoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEventoEquino.objects.all()
    serializer_class = CatalogoEventoEquinoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoSesionViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoSesion.objects.all()
    serializer_class = CatalogoEstadoSesionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoEstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoEstadoPago.objects.all()
    serializer_class = CatalogoEstadoPagoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

@extend_schema_view(
    list=extend_schema(tags=['Catálogos']),
    retrieve=extend_schema(tags=['Catálogos']),
    create=extend_schema(tags=['Catálogos']),
    update=extend_schema(tags=['Catálogos']),
    partial_update=extend_schema(tags=['Catálogos']),
    destroy=extend_schema(tags=['Catálogos']),
)
class CatalogoParentescoViewSet(viewsets.ModelViewSet):
    queryset = CatalogoParentesco.objects.all()
    serializer_class = CatalogoParentescoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import IsAdminOrTerapeuta
from api.models import Caballo, BitacoraEquina
from api.serializers import (
    CaballoSerializer, CaballoWriteSerializer,
    BitacoraEquinaSerializer, BitacoraEquinaWriteSerializer
)
from api.services.welfare_service import WelfareService

@extend_schema_view(
    list=extend_schema(tags=['Caballos']),
    retrieve=extend_schema(tags=['Caballos']),
    create=extend_schema(tags=['Caballos']),
    update=extend_schema(tags=['Caballos']),
    partial_update=extend_schema(tags=['Caballos']),
    destroy=extend_schema(tags=['Caballos']),
)
class CaballoViewSet(viewsets.ModelViewSet):
    queryset = Caballo.objects.all().order_by('-fecha_registro')
    serializer_class = CaballoSerializer
    permission_classes = [IsAdminOrTerapeuta]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CaballoWriteSerializer
        return CaballoSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        data = self.request.data
        if 'disponible' in data:
            disp = data.get('disponible')
            if isinstance(disp, str):
                disp = disp.lower() == 'true'
            
            instance.estado_salud_id = 1 if disp else 2
            if disp:
                instance.motivo_inactividad = None
            instance.save(update_fields=['estado_salud_id', 'motivo_inactividad'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response({"message": "Caballo dado de baja (borrado lógico)."}, status=status.HTTP_200_OK)

@extend_schema_view(
    list=extend_schema(tags=['Caballos']),
    retrieve=extend_schema(tags=['Caballos']),
    create=extend_schema(tags=['Caballos']),
    update=extend_schema(tags=['Caballos']),
    partial_update=extend_schema(tags=['Caballos']),
    destroy=extend_schema(tags=['Caballos']),
)
class BitacoraEquinaViewSet(viewsets.ModelViewSet):
    queryset = BitacoraEquina.objects.all().order_by('-fecha_evento', '-hora_evento', '-fecha_registro')
    serializer_class = BitacoraEquinaSerializer
    filterset_fields = ['caballo']
    permission_classes = [IsAdminOrTerapeuta]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BitacoraEquinaWriteSerializer
        return BitacoraEquinaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        caballo_id = self.request.query_params.get('caballo')
        if caballo_id:
            qs = qs.filter(caballo_id=caballo_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def caballo_disponibilidad(request):
    """
    GET /api/caballo-disponibilidad/?caballo_id=X&fecha=YYYY-MM-DD&hora=HH:MM&duracion=60
    """
    caballo_id = request.query_params.get('caballo_id')
    fecha      = request.query_params.get('fecha')
    hora       = request.query_params.get('hora', '09:00')
    duracion   = request.query_params.get('duracion', 60)
    
    try:
        duracion = int(duracion)
    except (ValueError, TypeError):
        duracion = 60

    if not caballo_id:
        return Response({"error": "Se requiere caballo_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        resp = WelfareService.check_caballo_disponibilidad(caballo_id, fecha, hora, duracion)
        return Response(resp)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

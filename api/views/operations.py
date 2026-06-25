from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.models import Sesion, ReporteSesion, ReporteObjetivo
from api.serializers import (
    SesionSerializer, SesionWriteSerializer,
    ReporteSesionSerializer, ReporteSesionWriteSerializer,
    TutorReporteSesionSerializer, ReporteObjetivoSerializer
)
from api.services.session_service import SessionService

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.select_related('paciente', 'terapeuta', 'terapeuta__usuario', 'caballo', 'estatus').all().order_by('-fecha_hora')
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            return qs.none()
            
        rol_nombre = getattr(self.request.user.rol, 'nombre', '')
        
        if not self.request.user.is_staff:
            if rol_nombre == 'Terapeuta':
                qs = qs.filter(terapeuta__usuario=self.request.user)
            elif rol_nombre in ['Tutor', 'Paciente']:
                qs = qs.filter(paciente__tutor=self.request.user)

        # Filtro de archivadas (borrado lógico)
        archivada_param = self.request.query_params.get('archivada')
        if archivada_param == 'true':
            qs = qs.filter(archivada=True)
        else:
            qs = qs.filter(archivada=False)

        fecha = self.request.query_params.get('fecha')
        if fecha:
            qs = qs.filter(fecha_hora__date=fecha)

        return qs

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SesionWriteSerializer
        return SesionSerializer

    def create(self, request, *args, **kwargs):
        caballo_id   = request.data.get('caballo')
        paciente_id  = request.data.get('paciente')
        terapeuta_id = request.data.get('terapeuta')
        fecha_hora   = request.data.get('fecha_hora')
        
        try:
            duracion_min = int(request.data.get('duracion_minutos', 60))
        except (ValueError, TypeError):
            duracion_min = 60

        try:
            SessionService.validate_session(
                caballo_id=caballo_id,
                paciente_id=paciente_id,
                terapeuta_id=terapeuta_id,
                fecha_hora_str=fecha_hora,
                duracion_minutos=duracion_min,
                exclude_id=request.data.get('exclude_id')
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # We also validate on update
        caballo_id   = request.data.get('caballo') or self.get_object().caballo_id
        paciente_id  = request.data.get('paciente') or self.get_object().paciente_id
        terapeuta_id = request.data.get('terapeuta') or self.get_object().terapeuta_id
        fecha_hora   = request.data.get('fecha_hora') or self.get_object().fecha_hora.strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            duracion_min = int(request.data.get('duracion_minutos', self.get_object().duracion_minutos))
        except (ValueError, TypeError):
            duracion_min = 60

        try:
            SessionService.validate_session(
                caballo_id=caballo_id,
                paciente_id=paciente_id,
                terapeuta_id=terapeuta_id,
                fecha_hora_str=fecha_hora,
                duracion_minutos=duracion_min,
                exclude_id=self.get_object().id
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        return super().update(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class ReporteSesionViewSet(viewsets.ModelViewSet):
    queryset = ReporteSesion.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            return qs.none()
            
        rol_nombre = getattr(self.request.user.rol, 'nombre', '')
        
        if not self.request.user.is_staff:
            if rol_nombre == 'Terapeuta':
                return qs.filter(sesion__terapeuta__usuario=self.request.user)
            elif rol_nombre in ['Tutor', 'Paciente']:
                return qs.filter(sesion__paciente__tutor=self.request.user)
        return qs

    def get_serializer_class(self):
        rol_nombre = getattr(self.request.user.rol, 'nombre', '') if not self.request.user.is_anonymous else ''
        if not self.request.user.is_staff and rol_nombre in ['Tutor', 'Paciente']:
            return TutorReporteSesionSerializer
        
        if self.action in ['create', 'update', 'partial_update']:
            return ReporteSesionWriteSerializer
        return ReporteSesionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            payload = {
                "nombre_paciente": instance.sesion.paciente.nombre,
                "telefono_tutor": instance.sesion.paciente.tutor.telefono,
                "recomendacion_casa": instance.recomendacion_casa,
                "objetivos_trabajados": "N/A"
            }
            print("Webhook disparado a n8n:", payload)
        except Exception as e:
            print("Error disparando webhook:", e)

@extend_schema_view(
    list=extend_schema(tags=['Sesiones']),
    retrieve=extend_schema(tags=['Sesiones']),
    create=extend_schema(tags=['Sesiones']),
    update=extend_schema(tags=['Sesiones']),
    partial_update=extend_schema(tags=['Sesiones']),
    destroy=extend_schema(tags=['Sesiones']),
)
class ReporteObjetivoViewSet(viewsets.ModelViewSet):
    queryset = ReporteObjetivo.objects.all()
    serializer_class = ReporteObjetivoSerializer
    permission_classes = [IsAuthenticated]

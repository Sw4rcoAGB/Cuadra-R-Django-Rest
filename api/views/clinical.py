from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import IsAdmin, IsAdminOrTerapeuta
from api.models import Terapeuta, Paciente, PacienteDiagnostico, ContactoEmergencia
from api.serializers import (
    TerapeutaSerializer, PacienteSerializer, PacienteDiagnosticoSerializer, ContactoEmergenciaSerializer
)
from api.services.patient_service import PatientService
from api.services.staff_service import StaffService

@extend_schema_view(
    list=extend_schema(tags=['Usuarios']),
    retrieve=extend_schema(tags=['Usuarios']),
    create=extend_schema(tags=['Usuarios']),
    update=extend_schema(tags=['Usuarios']),
    partial_update=extend_schema(tags=['Usuarios']),
    destroy=extend_schema(tags=['Usuarios']),
)
class TerapeutaViewSet(viewsets.ModelViewSet):
    queryset = Terapeuta.objects.all()
    serializer_class = TerapeutaSerializer
    permission_classes = [IsAdminOrTerapeuta]
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        usuario = instance.usuario
        usuario.activo = False
        usuario.save()
        return Response({"message": "Terapeuta dado de baja (borrado logico)."}, status=status.HTTP_200_OK)

@extend_schema(tags=['Usuarios'])
@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAdmin])
def registrar_terapeuta(request, pk=None):
    try:
        terapeuta = StaffService.registrar_terapeuta(request.data, pk)
        message = "Terapeuta actualizado exitosamente." if pk else "Terapeuta creado exitosamente."
        return Response({"message": message, "id": str(terapeuta.id)}, status=status.HTTP_201_CREATED if not pk else status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        rol = getattr(self.request.user, 'rol', None)
        rol_nombre = getattr(rol, 'nombre', '') if rol else ''

        # Tutores solo ven sus propios pacientes
        if rol_nombre in ['Tutor', 'Paciente']:
            return qs.filter(tutor=self.request.user, activo=True)

        # Admin puede ver inactivos con ?activo=false
        activo_param = self.request.query_params.get('activo', 'true')
        if activo_param.lower() == 'false':
            return qs.filter(activo=False)

        # Por defecto, terapeuta y admin solo ven activos
        return qs.filter(activo=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response({"message": "Paciente dado de baja (borrado lógico)."}, status=status.HTTP_200_OK)

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class PacienteDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = PacienteDiagnostico.objects.all()
    serializer_class = PacienteDiagnosticoSerializer
    permission_classes = [IsAdminOrTerapeuta]

@extend_schema_view(
    list=extend_schema(tags=['Pacientes']),
    retrieve=extend_schema(tags=['Pacientes']),
    create=extend_schema(tags=['Pacientes']),
    update=extend_schema(tags=['Pacientes']),
    partial_update=extend_schema(tags=['Pacientes']),
    destroy=extend_schema(tags=['Pacientes']),
)
class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.all()
    serializer_class = ContactoEmergenciaSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=['Pacientes'])
@api_view(['POST'])
@permission_classes([IsAdmin])
def registrar_paciente(request):
    try:
        paciente = PatientService.registrar_paciente(request.data)
        return Response({
            "message": "Expediente registrado exitosamente.",
            "id": str(paciente.id),
            "paciente": {"nombre": paciente.nombre, "id": str(paciente.id)}
        }, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

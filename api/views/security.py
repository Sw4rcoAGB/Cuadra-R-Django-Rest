from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action as drf_action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import IsAdmin
from api.models import Usuario, BitacoraSeguridad
from api.serializers import UsuarioSerializer, BitacoraSeguridadSerializer
from api.services.auth_service import AuthService

@extend_schema_view(
    list=extend_schema(tags=['Usuarios']),
    retrieve=extend_schema(tags=['Usuarios']),
    create=extend_schema(tags=['Usuarios']),
    update=extend_schema(tags=['Usuarios']),
    partial_update=extend_schema(tags=['Usuarios']),
    destroy=extend_schema(tags=['Usuarios']),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]  # Only Admin can list/manage all users

    @drf_action(detail=True, methods=['post'], url_path='cambiar-contrasena', permission_classes=[IsAuthenticated])
    def cambiar_contrasena(self, request, pk=None):
        usuario = self.get_object()
        # Non-admins can only change their own password
        if request.user.rol.nombre not in ('Admin', 'Administrador') and request.user.id != usuario.id:
            return Response({'error': 'No tienes permiso para cambiar la contraseña de este usuario.'}, status=status.HTTP_403_FORBIDDEN)
            
        actual = request.data.get('password_actual', '')
        nueva = request.data.get('password_nueva', '')
        if not check_password(actual, usuario.password):
            return Response({'error': 'Contraseña actual incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(nueva) < 8:
            return Response({'error': 'La nueva contraseña debe tener al menos 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        usuario.password = make_password(nueva)
        usuario.save()
        return Response({'message': 'Contraseña actualizada correctamente.'})

@extend_schema_view(
    list=extend_schema(tags=['Auditoría']),
    retrieve=extend_schema(tags=['Auditoría']),
)
class BitacoraSeguridadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BitacoraSeguridad.objects.select_related('usuario_afectado', 'usuario_accion').all()
    serializer_class = BitacoraSeguridadSerializer
    permission_classes = [IsAdmin]

# ==========================================
# AUTHENTICATION
# ==========================================
@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint — devuelve access_token (JWT 12h) + refresh_token (7d).
    """
    from api.jwt_serializers import CuadraTokenObtainPairSerializer
    serializer = CuadraTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({
            "message": "Login exitoso",
            "access":  data['access'],
            "refresh": data['refresh'],
            "user":    data['user'],
        }, status=status.HTTP_200_OK)
    
    errors = serializer.errors
    detail = errors.get('detail') or errors.get('non_field_errors') or str(errors)
    if isinstance(detail, list):
        detail = detail[0]
    return Response({"error": str(detail)}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=['Usuarios'])
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Generates a magic link token and sends it."""
    email = request.data.get('email', '').strip()
    try:
        AuthService.forgot_password(email)
        return Response({"message": "¡Enlace de seguridad enviado con éxito!"}, status=status.HTTP_200_OK)
    except ValueError as e:
        status_code = status.HTTP_400_BAD_REQUEST if "requerido" in str(e) else status.HTTP_404_NOT_FOUND
        return Response({"error": str(e)}, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_magic(request):
    """Consumes the magic link token and sets a new password."""
    token_id = request.data.get('token')
    new_password = request.data.get('new_password')
    try:
        AuthService.reset_password_magic(token_id, new_password)
        return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resetear_password(request, usuario_id):
    nueva_password = request.data.get('new_password') or request.data.get('password')
    try:
        # Non-admins can only reset their own password (though admins usually reset others)
        if request.user.rol.nombre not in ('Admin', 'Administrador') and request.user.id != usuario_id:
            return Response({'error': 'No tienes permiso para reestablecer esta contraseña.'}, status=status.HTTP_403_FORBIDDEN)

        AuthService.resetear_password(usuario_id, nueva_password)
        return Response({"message": "Contraseña actualizada correctamente."})
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Usuarios'])
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request, usuario_id):
    """Update user profile (name, email, phone)."""
    # Check authorization
    if request.user.rol.nombre not in ('Admin', 'Administrador') and request.user.id != usuario_id:
        return Response({'error': 'No tienes permiso para actualizar este perfil.'}, status=status.HTTP_403_FORBIDDEN)
        
    try:
        usuario = AuthService.update_profile(usuario_id, request.data)
        return Response({
            "message": "Perfil actualizado correctamente.",
            "user": {
                "id": str(usuario.id),
                "nombre": usuario.nombre_completo,
                "email": usuario.email,
                "rol": usuario.rol.nombre
            }
        })
    except ValueError as e:
        status_code = status.HTTP_400_BAD_REQUEST if "uso" in str(e) else status.HTTP_404_NOT_FOUND
        return Response({"error": str(e)}, status=status_code)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request, usuario_id):
    """Change password with current password verification."""
    # Check authorization
    if request.user.id != usuario_id:
        return Response({'error': 'No tienes permiso para cambiar la contraseña de este usuario.'}, status=status.HTTP_403_FORBIDDEN)
        
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    try:
        AuthService.change_password(
            usuario_id=usuario_id,
            current_password=current_password,
            new_password=new_password,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return Response({"message": "Contraseña actualizada correctamente."})
    except ValueError as e:
        status_code = status.HTTP_400_BAD_REQUEST
        return Response({"error": str(e)}, status=status_code)
    except PermissionError as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

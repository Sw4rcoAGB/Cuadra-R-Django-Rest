"""
Cuadra Erre — Permisos RBAC
Clases de permisos reutilizables basadas en roles.
Se aplican en los ViewSets para controlar el acceso.
"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Permite acceso solo a usuarios con rol Admin/Administrador."""
    message = "Solo los administradores pueden realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        rol = getattr(request.user, 'rol', None)
        if not rol:
            return False
        return rol.nombre in ('Admin', 'Administrador')


class IsTerapeuta(BasePermission):
    """Permite acceso solo a terapeutas."""
    message = "Solo los terapeutas pueden realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        rol = getattr(request.user, 'rol', None)
        if not rol:
            return False
        return rol.nombre == 'Terapeuta'


class IsAdminOrTerapeuta(BasePermission):
    """Permite acceso a Admin o Terapeuta."""
    message = "Solo administradores y terapeutas pueden realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        rol = getattr(request.user, 'rol', None)
        if not rol:
            return False
        return rol.nombre in ('Admin', 'Administrador', 'Terapeuta')


class IsTutorOrPaciente(BasePermission):
    """Permite acceso a Tutores y Pacientes."""
    message = "Solo tutores y pacientes pueden realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        rol = getattr(request.user, 'rol', None)
        if not rol:
            return False
        return rol.nombre in ('Tutor', 'Paciente')


class IsAdminOrReadOnly(BasePermission):
    """
    Admin puede hacer cualquier cosa.
    El resto solo puede leer (GET, HEAD, OPTIONS).
    Útil para catálogos: cualquiera autenticado los lee, solo admin los edita.
    """
    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        rol = getattr(request.user, 'rol', None)
        if not rol:
            return False
        return rol.nombre in ('Admin', 'Administrador')


class IsOwnerOrAdmin(BasePermission):
    """
    Para objetos que tienen un 'usuario' o 'tutor':
    el dueño puede verlo/editarlo, admin puede ver/editar todo.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or request.user.is_anonymous:
            return False
        rol = getattr(request.user, 'rol', None)
        if rol and rol.nombre in ('Admin', 'Administrador'):
            return True
        # Verificar propiedad
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        if hasattr(obj, 'tutor'):
            return obj.tutor == request.user
        return False

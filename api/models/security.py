import uuid
from django.db import models

# ==========================================
# MÓDULO 1: SEGURIDAD (RBAC)
# ==========================================
class Rol(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Admin, Terapeuta, Tutor

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) # Hash
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    # DRF Compatibility Properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return self.rol.nombre == 'Admin'

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.nombre_completo

class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    utilizado = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        import datetime
        # Válido por 1 hora
        return not self.utilizado and (timezone.now() - self.creado_en) < datetime.timedelta(hours=1)

class BitacoraSeguridad(models.Model):
    TIPOS_EVENTO = (
        ('LOGIN', 'Inicio de Sesión'),
        ('PASSWORD_CHANGE', 'Cambio de Contraseña'),
        ('ARCHIVE', 'Registro Archivado'),
        ('RESTORE', 'Registro Restaurado'),
        ('CRITICAL_CONFIG', 'Cambio en Configuración Crítica'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_afectado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_recibidos')
    usuario_accion = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='eventos_realizados')
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bitácora de Seguridad"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.tipo_evento} - {self.usuario_afectado.email} - {self.fecha_hora}"

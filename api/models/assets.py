import uuid
from django.db import models
from .catalogs import CatalogoEstadoCaballo, CatalogoEventoEquino

# ==========================================
# MÓDULO 5: ACTIVOS Y BIENESTAR ANIMAL
# ==========================================
class Caballo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado_salud = models.ForeignKey(CatalogoEstadoCaballo, on_delete=models.PROTECT)
    peso_max_soporta = models.DecimalField(max_digits=5, decimal_places=2)
    sesiones_semanales_max = models.IntegerField()
    raza = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    motivo_inactividad = models.CharField(max_length=255, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='caballos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class BitacoraEquina(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caballo = models.ForeignKey(Caballo, on_delete=models.PROTECT)
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_evento = models.DateField(null=True, blank=True)
    hora_evento = models.TimeField(null=True, blank=True)
    tipo_evento = models.ForeignKey(CatalogoEventoEquino, on_delete=models.PROTECT)
    descripcion_veterinaria = models.TextField()

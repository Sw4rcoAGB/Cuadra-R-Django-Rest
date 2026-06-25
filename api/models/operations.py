import uuid
from django.db import models
from .clinical import Paciente, Terapeuta
from .assets import Caballo
from .catalogs import CatalogoEstadoSesion, CatalogoObjetivo

# ==========================================
# MÓDULO 6: OPERACIÓN CLÍNICA (CORE)
# ==========================================
class Sesion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.PROTECT)
    caballo = models.ForeignKey(Caballo, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(default=60, help_text="Duración de la sesión en minutos")
    estatus = models.ForeignKey(CatalogoEstadoSesion, on_delete=models.PROTECT)
    archivada = models.BooleanField(default=False, help_text="Borrado lógico")

    def __str__(self):
        return f"Sesion: {self.paciente.nombre} - {self.fecha_hora.strftime('%d/%m/%Y')}"

class ReporteSesion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sesion = models.OneToOneField(Sesion, on_delete=models.PROTECT)
    ansiedad_inicial = models.IntegerField(help_text="Escala del 1 al 10")
    ansiedad_final = models.IntegerField(help_text="Escala del 1 al 10")
    notas_clinicas = models.TextField()
    recomendacion_casa = models.TextField()

class ReporteObjetivo(models.Model):
    reporte = models.ForeignKey(ReporteSesion, on_delete=models.CASCADE)
    objetivo = models.ForeignKey(CatalogoObjetivo, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('reporte', 'objetivo')

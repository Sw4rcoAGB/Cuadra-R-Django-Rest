import uuid
from django.db import models
from .security import Usuario
from .assets import Caballo
from .catalogs import CatalogoDiagnostico, CatalogoParentesco

# ==========================================
# MÓDULO 3: EQUIPO CLÍNICO
# ==========================================
class Terapeuta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    especialidad_text = models.CharField(max_length=255, blank=True, null=True)
    rfc = models.CharField(max_length=20, blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=255, blank=True, null=True)
    cedula_profesional = models.CharField(max_length=50, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=True)  # Switch: vacaciones/fuera de servicio
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.especialidad_text or self.carrera}"

# ==========================================
# MÓDULO 4: PACIENTES Y FAMILIAS
# ==========================================
class Paciente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pacientes_tutorados')
    caballo_favorito = models.ForeignKey(Caballo, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    
    # Historial Clínico
    es_mayor_de_edad = models.BooleanField(default=False)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    ocupacion_escolaridad = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=255, blank=True, null=True)
    tutor_secundario_nombre = models.CharField(max_length=255, blank=True, null=True)
    tutor_secundario_telefono = models.CharField(max_length=20, blank=True, null=True)
    motivo_consulta = models.TextField(blank=True, null=True)
    historial_medico = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class PacienteDiagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    diagnostico = models.ForeignKey(CatalogoDiagnostico, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('paciente', 'diagnostico')

class ContactoEmergencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    parentesco = models.ForeignKey(CatalogoParentesco, on_delete=models.PROTECT)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

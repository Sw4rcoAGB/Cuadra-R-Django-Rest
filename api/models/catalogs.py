from django.db import models

# ==========================================
# MÓDULO 2: CATÁLOGOS MAESTROS
# ==========================================
class CatalogoEspecialidad(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Fisioterapia, Psicología
    def __str__(self): return self.nombre

class CatalogoDiagnostico(models.Model):
    nombre = models.CharField(max_length=100) # Ej: PCI, TEA, Síndrome de Down
    def __str__(self): return self.nombre

class CatalogoObjetivo(models.Model):
    nombre = models.CharField(max_length=255) # Ej: Mejorar equilibrio
    def __str__(self): return self.nombre

class CatalogoEstadoCaballo(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Activo, Reposo, Atención Médica
    def __str__(self): return self.nombre

class CatalogoEventoEquino(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Vacuna, Herraje, Lesión
    def __str__(self): return self.nombre

class CatalogoEstadoSesion(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Programada, En Curso, Finalizada, Cancelada
    def __str__(self): return self.nombre

class CatalogoEstadoPago(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Pendiente, Pagado, Vencido, Condonado
    def __str__(self): return self.nombre

class CatalogoParentesco(models.Model):
    nombre = models.CharField(max_length=50) # Ej: Madre, Padre, Abuelo/a, Tutor Legal
    def __str__(self): return self.nombre

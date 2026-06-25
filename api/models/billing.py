import uuid
from django.db import models
from .security import Usuario
from .operations import Sesion
from .catalogs import CatalogoEstadoPago

# ==========================================
# MÓDULO 7: ADMINISTRACIÓN FINANCIERA
# ==========================================
class Pago(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pagos_tutor')
    sesion = models.ForeignKey(Sesion, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.ForeignKey(CatalogoEstadoPago, on_delete=models.PROTECT)
    fecha_limite = models.DateField()
    fecha_pago = models.DateField(auto_now_add=True, null=True, blank=True)
    comprobante = models.FileField(upload_to='pagos/', blank=True, null=True)

    def __str__(self):
        return f"Pago: {self.tutor.nombre_completo} - ${self.monto}"

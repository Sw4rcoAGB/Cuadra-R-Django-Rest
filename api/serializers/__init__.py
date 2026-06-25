# api/serializers/__init__.py
# Exponer todos los serializadores para mantener compatibilidad.

from .catalogs import (
    RolSerializer,
    CatalogoEspecialidadSerializer,
    CatalogoDiagnosticoSerializer,
    CatalogoObjetivoSerializer,
    CatalogoEstadoCaballoSerializer,
    CatalogoEventoEquinoSerializer,
    CatalogoEstadoSesionSerializer,
    CatalogoEstadoPagoSerializer,
    CatalogoParentescoSerializer,
)
from .security import UsuarioSerializer, BitacoraSeguridadSerializer
from .assets import (
    CaballoSerializer,
    CaballoWriteSerializer,
    BitacoraEquinaSerializer,
    BitacoraEquinaWriteSerializer,
)
from .clinical import (
    TerapeutaSerializer,
    PacienteSerializer,
    PacienteDiagnosticoSerializer,
    ContactoEmergenciaSerializer,
)
from .operations import (
    SesionSerializer,
    SesionWriteSerializer,
    ReporteSesionSerializer,
    ReporteSesionWriteSerializer,
    TutorReporteSesionSerializer,
    ReporteObjetivoSerializer,
)
from .billing import PagoSerializer

__all__ = [
    'RolSerializer',
    'CatalogoEspecialidadSerializer',
    'CatalogoDiagnosticoSerializer',
    'CatalogoObjetivoSerializer',
    'CatalogoEstadoCaballoSerializer',
    'CatalogoEventoEquinoSerializer',
    'CatalogoEstadoSesionSerializer',
    'CatalogoEstadoPagoSerializer',
    'CatalogoParentescoSerializer',
    'UsuarioSerializer',
    'BitacoraSeguridadSerializer',
    'CaballoSerializer',
    'CaballoWriteSerializer',
    'BitacoraEquinaSerializer',
    'BitacoraEquinaWriteSerializer',
    'TerapeutaSerializer',
    'PacienteSerializer',
    'PacienteDiagnosticoSerializer',
    'ContactoEmergenciaSerializer',
    'SesionSerializer',
    'SesionWriteSerializer',
    'ReporteSesionSerializer',
    'ReporteSesionWriteSerializer',
    'TutorReporteSesionSerializer',
    'ReporteObjetivoSerializer',
    'PagoSerializer',
]

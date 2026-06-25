# api/models/__init__.py
# Exponer todos los modelos para mantener la compatibilidad con importaciones externas y migraciones de Django.

from .security import Rol, Usuario, PasswordResetToken, BitacoraSeguridad
from .catalogs import (
    CatalogoEspecialidad,
    CatalogoDiagnostico,
    CatalogoObjetivo,
    CatalogoEstadoCaballo,
    CatalogoEventoEquino,
    CatalogoEstadoSesion,
    CatalogoEstadoPago,
    CatalogoParentesco,
)
from .assets import Caballo, BitacoraEquina
from .clinical import Terapeuta, Paciente, PacienteDiagnostico, ContactoEmergencia
from .operations import Sesion, ReporteSesion, ReporteObjetivo
from .billing import Pago

__all__ = [
    'Rol',
    'Usuario',
    'PasswordResetToken',
    'BitacoraSeguridad',
    'CatalogoEspecialidad',
    'CatalogoDiagnostico',
    'CatalogoObjetivo',
    'CatalogoEstadoCaballo',
    'CatalogoEventoEquino',
    'CatalogoEstadoSesion',
    'CatalogoEstadoPago',
    'CatalogoParentesco',
    'Caballo',
    'BitacoraEquina',
    'Terapeuta',
    'Paciente',
    'PacienteDiagnostico',
    'ContactoEmergencia',
    'Sesion',
    'ReporteSesion',
    'ReporteObjetivo',
    'Pago',
]

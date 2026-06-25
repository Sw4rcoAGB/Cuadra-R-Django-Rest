# api/views/__init__.py
# Exponer todas las vistas y ViewSets para mantener compatibilidad con urls.py

from .catalogs import (
    RolViewSet,
    CatalogoEspecialidadViewSet,
    CatalogoDiagnosticoViewSet,
    CatalogoObjetivoViewSet,
    CatalogoEstadoCaballoViewSet,
    CatalogoEventoEquinoViewSet,
    CatalogoEstadoSesionViewSet,
    CatalogoEstadoPagoViewSet,
    CatalogoParentescoViewSet,
)
from .security import (
    UsuarioViewSet,
    BitacoraSeguridadViewSet,
    login_view,
    forgot_password,
    reset_password_magic,
    resetear_password,
    update_profile,
    change_password,
)
from .clinical import (
    TerapeutaViewSet,
    registrar_terapeuta,
    PacienteViewSet,
    PacienteDiagnosticoViewSet,
    ContactoEmergenciaViewSet,
    registrar_paciente,
)
from .assets import (
    CaballoViewSet,
    BitacoraEquinaViewSet,
    caballo_disponibilidad,
)
from .operations import (
    SesionViewSet,
    ReporteSesionViewSet,
    ReporteObjetivoViewSet,
)
from .billing import (
    PagoViewSet,
)
from .dashboard import (
    dashboard_stats,
)

__all__ = [
    'RolViewSet',
    'CatalogoEspecialidadViewSet',
    'CatalogoDiagnosticoViewSet',
    'CatalogoObjetivoViewSet',
    'CatalogoEstadoCaballoViewSet',
    'CatalogoEventoEquinoViewSet',
    'CatalogoEstadoSesionViewSet',
    'CatalogoEstadoPagoViewSet',
    'CatalogoParentescoViewSet',
    'UsuarioViewSet',
    'BitacoraSeguridadViewSet',
    'login_view',
    'forgot_password',
    'reset_password_magic',
    'resetear_password',
    'update_profile',
    'change_password',
    'TerapeutaViewSet',
    'registrar_terapeuta',
    'PacienteViewSet',
    'PacienteDiagnosticoViewSet',
    'ContactoEmergenciaViewSet',
    'registrar_paciente',
    'CaballoViewSet',
    'BitacoraEquinaViewSet',
    'caballo_disponibilidad',
    'SesionViewSet',
    'ReporteSesionViewSet',
    'ReporteObjetivoViewSet',
    'PagoViewSet',
    'dashboard_stats',
]

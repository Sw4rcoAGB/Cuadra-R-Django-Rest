import pytest
from datetime import timedelta
from django.utils import timezone
from api.models import Rol, Usuario, Paciente, Terapeuta, Caballo, Sesion, CatalogoEstadoCaballo, CatalogoEstadoSesion
from api.services.welfare_service import WelfareService
from api.services.session_service import SessionService

@pytest.mark.django_db
class TestSessionServices:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        # Setup roles
        self.tutor_role, _ = Rol.objects.get_or_create(nombre='Tutor')
        self.terapeuta_role, _ = Rol.objects.get_or_create(nombre='Terapeuta')
        
        # Setup statuses
        self.health_active, _ = CatalogoEstadoCaballo.objects.get_or_create(nombre='Activo')
        self.health_resting, _ = CatalogoEstadoCaballo.objects.get_or_create(nombre='Reposo')
        self.session_scheduled, _ = CatalogoEstadoSesion.objects.get_or_create(nombre='Programada')
        
        # Setup horses
        self.caballo = Caballo.objects.create(
            nombre="Centella",
            estado_salud=self.health_active,
            peso_max_soporta=80.0,
            sesiones_semanales_max=3
        )
        
        # Setup users and patient/therapist
        self.tutor_user = Usuario.objects.create(
            rol=self.tutor_role,
            email="tutor@example.com",
            nombre_completo="Tutor Perez"
        )
        self.paciente = Paciente.objects.create(
            tutor=self.tutor_user,
            nombre="Juanito",
            fecha_nacimiento="2015-01-01",
            peso_kg=45.0
        )
        
        self.terapeuta_user = Usuario.objects.create(
            rol=self.terapeuta_role,
            email="terapeuta@example.com",
            nombre_completo="Licenciado Gomez"
        )
        self.terapeuta = Terapeuta.objects.create(
            usuario=self.terapeuta_user
        )

    def test_validate_session_success(self):
        # 1. Active horse, correct weight, no collisions
        fecha_str = "2026-07-01T10:00:00"
        SessionService.validate_session(
            caballo_id=self.caballo.id,
            paciente_id=self.paciente.id,
            terapeuta_id=self.terapeuta.id,
            fecha_hora_str=fecha_str
        )

    def test_validate_session_welfare_inactive_horse(self):
        # 2. Horse is in reposo
        self.caballo.estado_salud = self.health_resting
        self.caballo.save()
        
        fecha_str = "2026-07-01T10:00:00"
        with pytest.raises(ValueError, match="no está en estado Activo"):
            SessionService.validate_session(
                caballo_id=self.caballo.id,
                paciente_id=self.paciente.id,
                terapeuta_id=self.terapeuta.id,
                fecha_hora_str=fecha_str
            )

    def test_validate_session_welfare_weight_limit(self):
        # 3. Patient weight exceeds horse limit
        self.paciente.peso_kg = 95.0
        self.paciente.save()
        
        fecha_str = "2026-07-01T10:00:00"
        with pytest.raises(ValueError, match="supera el peso máximo"):
            SessionService.validate_session(
                caballo_id=self.caballo.id,
                paciente_id=self.paciente.id,
                terapeuta_id=self.terapeuta.id,
                fecha_hora_str=fecha_str
            )

    def test_validate_session_collision_horse(self):
        # 4. Schedule a session that overlaps
        fecha = timezone.make_aware(timezone.datetime(2026, 7, 1, 10, 0, 0), timezone.get_current_timezone())
        Sesion.objects.create(
            paciente=self.paciente,
            terapeuta=self.terapeuta,
            caballo=self.caballo,
            fecha_hora=fecha,
            duracion_minutos=60,
            estatus=self.session_scheduled
        )
        
        # Try to schedule another session for the horse at 10:30 (overlaps with 10:00-11:00)
        with pytest.raises(PermissionError, match="estará ocupado"):
            SessionService.validate_session(
                caballo_id=self.caballo.id,
                paciente_id=self.paciente.id,
                terapeuta_id=self.terapeuta.id,
                fecha_hora_str="2026-07-01T10:30:00"
            )

    def test_validate_session_weekly_limit(self):
        # 5. Fill up the horse's weekly limit (max 3)
        base_date = timezone.datetime(2026, 7, 1, 9, 0, 0)
        # Session 1
        Sesion.objects.create(
            paciente=self.paciente,
            terapeuta=self.terapeuta,
            caballo=self.caballo,
            fecha_hora=timezone.make_aware(base_date, timezone.get_current_timezone()),
            duracion_minutos=60,
            estatus=self.session_scheduled
        )
        # Session 2
        Sesion.objects.create(
            paciente=self.paciente,
            terapeuta=self.terapeuta,
            caballo=self.caballo,
            fecha_hora=timezone.make_aware(base_date + timedelta(days=1), timezone.get_current_timezone()),
            duracion_minutos=60,
            estatus=self.session_scheduled
        )
        # Session 3
        Sesion.objects.create(
            paciente=self.paciente,
            terapeuta=self.terapeuta,
            caballo=self.caballo,
            fecha_hora=timezone.make_aware(base_date + timedelta(days=2), timezone.get_current_timezone()),
            duracion_minutos=60,
            estatus=self.session_scheduled
        )
        
        # Try to validate a 4th session on the same week (should fail)
        with pytest.raises(PermissionError, match="alcanzó su límite"):
            SessionService.validate_session(
                caballo_id=self.caballo.id,
                paciente_id=self.paciente.id,
                terapeuta_id=self.terapeuta.id,
                fecha_hora_str="2026-07-01T15:00:00"
            )

    def test_check_caballo_disponibilidad_local(self):
        # Test availability reporting
        res = WelfareService.check_caballo_disponibilidad(self.caballo.id, "2026-07-01", "10:00", 60)
        assert res["disponible"] is True
        
        # Add conflict
        fecha = timezone.make_aware(timezone.datetime(2026, 7, 1, 10, 0, 0), timezone.get_current_timezone())
        Sesion.objects.create(
            paciente=self.paciente,
            terapeuta=self.terapeuta,
            caballo=self.caballo,
            fecha_hora=fecha,
            duracion_minutos=60,
            estatus=self.session_scheduled
        )
        
        res = WelfareService.check_caballo_disponibilidad(self.caballo.id, "2026-07-01", "10:30", 60)
        assert res["disponible"] is False
        assert res["ocupado_de"] == "10:00"

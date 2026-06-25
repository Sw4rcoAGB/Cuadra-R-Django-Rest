import pytest
from django.contrib.auth.hashers import check_password
from api.models import Usuario, Rol, Paciente, Terapeuta
from api.services.patient_service import PatientService
from api.services.staff_service import StaffService

@pytest.mark.django_db
class TestClinicalServices:
    @pytest.fixture(autouse=True)
    def setup_roles(self):
        self.admin_role, _ = Rol.objects.get_or_create(nombre='Admin')
        self.tutor_role, _ = Rol.objects.get_or_create(nombre='Tutor')
        self.terapeuta_role, _ = Rol.objects.get_or_create(nombre='Terapeuta')

    def test_registrar_paciente_success_minor(self):
        data = {
            "paciente_nombre": "pedrito gomez",
            "fecha_nacimiento": "2018-05-20",
            "peso_kg": "28.5",
            "es_mayor_de_edad": "false",
            "tutor_nombre": "tutor gomez",
            "tutor_email": "tutor.gomez@example.com",
            "tutor_password": "tutorpassword123",
            "tutor_telefono": "5512345678",
            "direccion": "calle falsa 123",
            "contacto_emergencia": "maria gomez"
        }
        
        paciente = PatientService.registrar_paciente(data)
        assert paciente.nombre == "Pedrito Gomez"
        assert paciente.tutor.email == "tutor.gomez@example.com"
        assert paciente.tutor.rol.nombre == "Tutor"
        assert check_password("tutorpassword123", paciente.tutor.password)
        assert Paciente.objects.filter(id=paciente.id).exists()

    def test_registrar_paciente_already_exists(self):
        data = {
            "paciente_nombre": "pedrito gomez",
            "fecha_nacimiento": "2018-05-20",
            "tutor_email": "tutor.gomez@example.com"
        }
        # First registration
        PatientService.registrar_paciente(data)
        # Second registration should fail
        with pytest.raises(ValueError, match="Ya existe un paciente"):
            PatientService.registrar_paciente(data)

    def test_registrar_terapeuta_success_new(self):
        data = {
            "nombre": "licenciada marcela",
            "email": "marcela@cuadraerre.com",
            "telefono": "987654321",
            "password": "securepassword",
            "carrera": "psicologia clinica",
            "especialidad_text": "terapia con caballos",
            "rfc": "MARC850101XX1",
            "cedula": "1234567"
        }
        
        terapeuta = StaffService.registrar_terapeuta(data)
        assert terapeuta.usuario.nombre_completo == "Licenciada Marcela"
        assert terapeuta.usuario.rol.nombre == "Terapeuta"
        assert terapeuta.carrera == "Psicologia Clinica"
        assert terapeuta.rfc == "MARC850101XX1"
        assert check_password("securepassword", terapeuta.usuario.password)

    def test_registrar_terapeuta_duplicate_rfc(self):
        data1 = {
            "nombre": "Terapeuta Uno",
            "email": "t1@cuadraerre.com",
            "password": "password",
            "rfc": "MARC850101XX1"
        }
        data2 = {
            "nombre": "Terapeuta Dos",
            "email": "t2@cuadraerre.com",
            "password": "password",
            "rfc": "MARC850101XX1"
        }
        StaffService.registrar_terapeuta(data1)
        with pytest.raises(ValueError, match="El RFC .* ya pertenece a otro terapeuta"):
            StaffService.registrar_terapeuta(data2)

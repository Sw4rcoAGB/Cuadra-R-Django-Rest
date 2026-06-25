from django.db import transaction
from django.contrib.auth.hashers import make_password
from api.models import Usuario, Rol, Paciente
from api.common.utils import cap, cap_sentence

class PatientService:
    @staticmethod
    def registrar_paciente(data):
        es_mayor_de_edad = str(data.get('es_mayor_de_edad', 'false')).lower() == 'true'
        paciente_nombre        = cap(data.get('paciente_nombre'))
        fecha_nacimiento       = data.get('fecha_nacimiento')
        peso_kg                = data.get('peso_kg')
        estado_civil           = cap(data.get('estado_civil'))
        ocupacion_escolaridad  = cap_sentence(data.get('ocupacion_escolaridad'))
        direccion              = cap(data.get('direccion'))
        contacto_emergencia    = cap(data.get('contacto_emergencia'))
        motivo_consulta        = cap_sentence(data.get('motivo_consulta'))
        historial_medico       = cap_sentence(data.get('historial_medico'))
        antecedentes_familiares= cap_sentence(data.get('antecedentes_familiares'))
        tutor_nombre           = cap(data.get('tutor_nombre'))
        tutor_email            = data.get('tutor_email')
        tutor_telefono         = data.get('tutor_telefono')
        tutor_password         = data.get('tutor_password')
        tutor2_nombre          = cap(data.get('tutor2_nombre'))
        tutor2_telefono        = data.get('tutor2_telefono')

        try:
            peso_kg = float(peso_kg) if peso_kg else 0.0
        except (ValueError, TypeError):
            peso_kg = 0.0

        if not all([paciente_nombre, fecha_nacimiento]):
            raise ValueError("Faltan campos obligatorios: nombre y fecha de nacimiento.")
        if not es_mayor_de_edad and not tutor_email:
            raise ValueError("Faltan campos obligatorios: email del tutor.")
        if es_mayor_de_edad and not tutor_email:
            raise ValueError("Debe proporcionar un email para el paciente.")

        if Paciente.objects.filter(nombre__iexact=paciente_nombre, fecha_nacimiento=fecha_nacimiento).exists():
            raise ValueError(f"Ya existe un paciente con el nombre '{paciente_nombre}' y la misma fecha de nacimiento.")

        cuenta_email    = tutor_email
        cuenta_nombre   = paciente_nombre if es_mayor_de_edad else (tutor_nombre or "Tutor de " + paciente_nombre)
        cuenta_telefono = tutor_telefono
        cuenta_password = tutor_password or "cuadra123"

        with transaction.atomic():
            usuario_tutor = Usuario.objects.filter(email=cuenta_email).first()

            if not usuario_tutor:
                nombre_rol = 'Paciente' if es_mayor_de_edad else 'Tutor'
                rol_obj, _ = Rol.objects.get_or_create(nombre=nombre_rol)
                usuario_tutor = Usuario.objects.create(
                    rol=rol_obj,
                    email=cuenta_email,
                    password=make_password(cuenta_password),
                    nombre_completo=cuenta_nombre,
                    telefono=cuenta_telefono
                )

            paciente = Paciente.objects.create(
                tutor=usuario_tutor,
                nombre=paciente_nombre,
                fecha_nacimiento=fecha_nacimiento,
                peso_kg=peso_kg,
                es_mayor_de_edad=es_mayor_de_edad,
                estado_civil=estado_civil,
                ocupacion_escolaridad=ocupacion_escolaridad,
                direccion=direccion,
                contacto_emergencia=contacto_emergencia,
                tutor_secundario_nombre=tutor2_nombre,
                tutor_secundario_telefono=tutor2_telefono,
                motivo_consulta=motivo_consulta,
                historial_medico=historial_medico,
                antecedentes_familiares=antecedentes_familiares
            )
        return paciente

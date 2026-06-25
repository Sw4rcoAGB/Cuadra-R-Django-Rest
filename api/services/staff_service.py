from django.db import transaction
from django.contrib.auth.hashers import make_password
from api.models import Usuario, Rol, Terapeuta
from api.common.utils import cap, cap_sentence

class StaffService:
    @staticmethod
    def registrar_terapeuta(data, pk=None):
        # Update existing therapist
        if pk:
            try:
                terapeuta = Terapeuta.objects.get(id=pk)
            except Terapeuta.DoesNotExist:
                raise ValueError("Terapeuta no encontrado.")
            
            usuario = terapeuta.usuario
            
            # Update Usuario
            usuario.nombre_completo = cap(data.get('nombre', usuario.nombre_completo))
            usuario.email = data.get('email', usuario.email)
            usuario.telefono = data.get('telefono', usuario.telefono)
            if data.get('password'):
                usuario.password = make_password(data.get('password'))
            usuario.save()

            # Update Terapeuta
            terapeuta.carrera = cap(data.get('carrera', terapeuta.carrera))
            terapeuta.especialidad_text = cap_sentence(data.get('especialidad_text', terapeuta.especialidad_text))
            
            rfc_val = data.get('rfc', terapeuta.rfc)
            terapeuta.rfc = rfc_val.upper() if rfc_val else rfc_val
            
            terapeuta.contacto_emergencia = cap(data.get('contacto_emergencia', terapeuta.contacto_emergencia))
            terapeuta.cedula_profesional = data.get('cedula', terapeuta.cedula_profesional)
            terapeuta.biografia = cap_sentence(data.get('biografia', terapeuta.biografia))
            
            if 'disponible' in data:
                terapeuta.disponible = data.get('disponible')
            terapeuta.save()
            return terapeuta

        # Create new therapist
        nombre = cap(data.get('nombre'))
        email = data.get('email')
        telefono = data.get('telefono')
        password = data.get('password')
        
        carrera = cap(data.get('carrera', ''))
        especialidad_text = cap_sentence(data.get('especialidad_text', ''))
        rfc = data.get('rfc', '').upper()
        contacto_emergencia = cap(data.get('contacto_emergencia', ''))
        cedula = data.get('cedula', '')
        biografia = cap_sentence(data.get('biografia', ''))

        if Usuario.objects.filter(email=email).exists():
            raise ValueError("El correo ya está registrado.")

        if rfc and Terapeuta.objects.filter(rfc__iexact=rfc).exists():
            raise ValueError(f"El RFC '{rfc}' ya pertenece a otro terapeuta.")

        with transaction.atomic():
            rol_terapeuta, _ = Rol.objects.get_or_create(nombre='Terapeuta')
            usuario = Usuario.objects.create(
                rol=rol_terapeuta,
                email=email,
                password=make_password(password),
                nombre_completo=nombre,
                telefono=telefono
            )
            terapeuta = Terapeuta.objects.create(
                usuario=usuario,
                carrera=carrera,
                especialidad_text=especialidad_text,
                rfc=rfc,
                contacto_emergencia=contacto_emergencia,
                cedula_profesional=cedula,
                biografia=biografia
            )
        return terapeuta

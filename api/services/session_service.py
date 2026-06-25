from datetime import timedelta
from django.utils import timezone
from dateutil import parser as dp
from api.models import Caballo, Paciente, Sesion, CatalogoEstadoSesion

class SessionService:
    @staticmethod
    def validate_session(caballo_id, paciente_id, terapeuta_id, fecha_hora_str, duracion_minutos=60, exclude_id=None):
        try:
            caballo  = Caballo.objects.get(id=caballo_id)
            paciente = Paciente.objects.get(id=paciente_id)
        except (Caballo.DoesNotExist, Paciente.DoesNotExist):
            raise ValueError("Caballo o Paciente no encontrado.")

        # ── Regla 1: Bienestar Animal ─────────────────────────────────────────
        if caballo.estado_salud.nombre.lower() != 'activo':
            raise ValueError("El caballo no está en estado Activo y no puede trabajar.")
            
        if paciente.peso_kg > caballo.peso_max_soporta:
            raise ValueError(f"El paciente ({paciente.peso_kg} kg) supera el peso máximo que soporta {caballo.nombre} ({caballo.peso_max_soporta} kg).")

        # ── Regla 2: Anti-Colisión con Duración ──────────────────────────────
        if fecha_hora_str:
            try:
                inicio_nueva = dp.parse(fecha_hora_str)
                if timezone.is_naive(inicio_nueva):
                    inicio_nueva = timezone.make_aware(inicio_nueva, timezone.get_current_timezone())
            except Exception:
                raise ValueError("Fecha/Hora de sesión inválida.")

            fin_nueva = inicio_nueva + timedelta(minutes=duracion_minutos)

            estatus_bloqueantes = CatalogoEstadoSesion.objects.filter(
                nombre__in=['Programada', 'En Curso']
            ).values_list('id', flat=True)

            # Conflictos del caballo
            conflictos_caballo = Sesion.objects.filter(
                caballo_id=caballo_id,
                estatus_id__in=estatus_bloqueantes,
            )
            if exclude_id:
                conflictos_caballo = conflictos_caballo.exclude(id=exclude_id)

            for s in conflictos_caballo:
                ini_s = s.fecha_hora
                if timezone.is_naive(ini_s):
                    ini_s = timezone.make_aware(ini_s, timezone.get_current_timezone())
                fin_s = ini_s + timedelta(minutes=s.duracion_minutos)
                if ini_s < fin_nueva and fin_s > inicio_nueva:
                    ini_fmt = ini_s.strftime("%H:%M")
                    fin_fmt = fin_s.strftime("%H:%M")
                    # We raise a custom exception or collision warning
                    raise PermissionError(f"🐴 {caballo.nombre} estará ocupado de {ini_fmt} a {fin_fmt}. Por favor elige otro horario, fecha o caballo.")

            # Conflictos del terapeuta
            conflictos_terapeuta = Sesion.objects.filter(
                terapeuta_id=terapeuta_id,
                estatus_id__in=estatus_bloqueantes,
            )
            if exclude_id:
                conflictos_terapeuta = conflictos_terapeuta.exclude(id=exclude_id)

            for s in conflictos_terapeuta:
                ini_s = s.fecha_hora
                if timezone.is_naive(ini_s):
                    ini_s = timezone.make_aware(ini_s, timezone.get_current_timezone())
                fin_s = ini_s + timedelta(minutes=s.duracion_minutos)
                if ini_s < fin_nueva and fin_s > inicio_nueva:
                    raise PermissionError("El terapeuta ya tiene otra sesión en ese horario.")

        # ── Regla 3: Límite semanal del caballo (máx 10/semana) ──────────────
        if fecha_hora_str:
            # Inicio de semana (lunes)
            inicio_semana = inicio_nueva - timedelta(days=inicio_nueva.weekday())
            inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_semana    = inicio_semana + timedelta(days=7)

            sesiones_semana = Sesion.objects.filter(
                caballo_id=caballo_id,
                fecha_hora__gte=inicio_semana,
                fecha_hora__lt=fin_semana,
            ).exclude(estatus__nombre__in=['Cancelada'])
            if exclude_id:
                sesiones_semana = sesiones_semana.exclude(id=exclude_id)

            sesiones_semana_count = sesiones_semana.count()

            max_semana = getattr(caballo, 'sesiones_semanales_max', 10) or 10
            if sesiones_semana_count >= max_semana:
                raise PermissionError(f"🐴 {caballo.nombre} ya alcanzó su límite de {max_semana} sesiones esta semana. Por favor elige otro caballo u otra semana.")

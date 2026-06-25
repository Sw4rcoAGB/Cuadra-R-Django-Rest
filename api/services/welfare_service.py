from datetime import timedelta
from django.utils import timezone
from dateutil import parser as dp
from api.models import Caballo, Sesion, CatalogoEstadoSesion

class WelfareService:
    @staticmethod
    def check_caballo_disponibilidad(caballo_id, fecha=None, hora=None, duracion=60):
        try:
            caballo = Caballo.objects.get(id=caballo_id)
        except Caballo.DoesNotExist:
            raise ValueError("Caballo no encontrado")

        # Sesiones de esta semana
        hoy = timezone.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_semana    = inicio_semana + timedelta(days=7)

        sesiones_semana = Sesion.objects.filter(
            caballo_id=caballo_id,
            fecha_hora__gte=inicio_semana,
            fecha_hora__lt=fin_semana,
        ).exclude(estatus__nombre__in=['Cancelada']).count()

        max_semana = getattr(caballo, 'sesiones_semanales_max', 10) or 10
        porcentaje = round((sesiones_semana / max_semana) * 100, 1) if max_semana > 0 else 0

        resp = {
            "disponible": True,
            "ocupado_de": None,
            "ocupado_hasta": None,
            "sesiones_semana": sesiones_semana,
            "max_semana": max_semana,
            "porcentaje_carga": porcentaje,
            "alcanzado_limite": sesiones_semana >= max_semana,
        }

        if fecha and hora:
            try:
                # Parse localized datetimes
                inicio_nueva = dp.parse(f"{fecha}T{hora}:00")
                if timezone.is_naive(inicio_nueva):
                    inicio_nueva = timezone.make_aware(inicio_nueva, timezone.get_current_timezone())
                fin_nueva    = inicio_nueva + timedelta(minutes=duracion)

                estatus_bloq = CatalogoEstadoSesion.objects.filter(
                    nombre__in=['Programada', 'En Curso']
                ).values_list('id', flat=True)

                for s in Sesion.objects.filter(caballo_id=caballo_id, estatus_id__in=estatus_bloq):
                    ini_s = s.fecha_hora
                    if timezone.is_naive(ini_s):
                        ini_s = timezone.make_aware(ini_s, timezone.get_current_timezone())
                    fin_s = ini_s + timedelta(minutes=s.duracion_minutos)
                    if ini_s < fin_nueva and fin_s > inicio_nueva:
                        local_ini = timezone.localtime(ini_s)
                        local_fin = timezone.localtime(fin_s)
                        resp["disponible"] = False
                        resp["ocupado_de"]    = local_ini.strftime("%H:%M")
                        resp["ocupado_hasta"] = local_fin.strftime("%H:%M")
                        break
            except Exception as e:
                print(f"Error parsing date/time in WelfareService: {e}")
                pass

        return resp

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.db.models import Count
from drf_spectacular.utils import extend_schema
import datetime
from api.permissions import IsAdmin
from api.models import Sesion, Paciente, Caballo, Terapeuta, ReporteSesion

@extend_schema(tags=['Auditoría'])
@api_view(['GET'])
@permission_classes([IsAdmin])
def dashboard_stats(request):
    """Returns real stats for the dashboard charts."""
    range_type = request.query_params.get('range', '30') # Default 30 days
    
    now = timezone.now()
    if range_type == '7':
        start_date = now - datetime.timedelta(days=7)
    elif range_type == '30':
        start_date = now - datetime.timedelta(days=30)
    else: # 'all' or others
        start_date = now - datetime.timedelta(days=365)

    # 1. Sesiones por día (Semana actual)
    sesiones_raw = Sesion.objects.filter(fecha_hora__gte=start_date)
    
    # Agrupar por día de la semana (Lunes a Sábado)
    dias_nombres = {0:'Lun', 1:'Mar', 2:'Mié', 3:'Jue', 4:'Vie', 5:'Sáb', 6:'Dom'}
    sesiones_por_dia = []
    for i in range(7):
        date_check = start_date + datetime.timedelta(days=i)
        count = sesiones_raw.filter(fecha_hora__date=date_check.date()).count()
        sesiones_por_dia.append({
            "name": dias_nombres[date_check.weekday()],
            "sesiones": count
        })

    # 2. Crecimiento de Pacientes (Últimos 4 meses)
    pacientes_crecimiento = []
    for i in range(4):
        month_check = (now.month - (3 - i) - 1) % 12 + 1
        year_check = now.year if month_check <= now.month else now.year - 1
        count = Paciente.objects.filter(fecha_registro__month__lte=month_check, fecha_registro__year__lte=year_check).count()
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        pacientes_crecimiento.append({
            "month": meses[month_check - 1],
            "total": count
        })

    # 3. Uso de Caballos (Top 5)
    uso_caballos = Caballo.objects.annotate(
        valor=Count('sesion')
    ).order_by('-valor')[:5].values('nombre', 'valor')
    uso_caballos_list = [{"name": c['nombre'], "valor": c['valor']} for c in uso_caballos]

    # 4. Distribución por Terapeuta
    dist_terapeutas = Terapeuta.objects.annotate(
        value=Count('sesion')
    ).values('usuario__nombre_completo', 'value')
    dist_terapeutas_list = [{"name": t['usuario__nombre_completo'].split(' ')[0], "value": t['value']} for t in dist_terapeutas]

    # --- MÉTRICAS CORE ---
    total_sesiones = Sesion.objects.count()
    total_pacientes = Paciente.objects.filter(activo=True).count()
    total_caballos = Caballo.objects.filter(activo=True).count()
    sesiones_hoy = Sesion.objects.filter(fecha_hora__date=now.date()).count()
    expertos_hoy = Terapeuta.objects.filter(usuario__activo=True, disponible=True).count()

    # --- NUEVAS MÉTRICAS REALES DE SALUD ---
    # A) Disponibilidad Real
    total_staff_activos = Terapeuta.objects.filter(usuario__activo=True).count() + total_caballos
    total_disponibles = expertos_hoy + Caballo.objects.filter(activo=True, disponible=True).count()
    disponibilidad_pct = int((total_disponibles / total_staff_activos * 100)) if total_staff_activos > 0 else 0

    # B) Asistencia Real (Sesiones Finalizadas / Totales pasadas)
    sesiones_pasadas = Sesion.objects.filter(fecha_hora__lte=now).count()
    sesiones_ok = Sesion.objects.filter(estatus__nombre__icontains='Finalizada').count()
    asistencia_pct = int((sesiones_ok / sesiones_pasadas * 100)) if sesiones_pasadas > 0 else 100

    # C) Cumplimiento (Simulado basado en si existen reportes para las sesiones)
    total_reportes = ReporteSesion.objects.count()
    cumplimiento_pct = int((total_reportes / total_sesiones * 100)) if total_sesiones > 0 else 0

    # D) Insight Dinámico
    insight = "La operación está estable. Todo el equipo está respondiendo bien."
    if disponibilidad_pct < 50:
        insight = "Atención: Menos de la mitad de tu equipo está disponible. Revisa las vacaciones."
    elif total_sesiones > 0 and total_reportes < (total_sesiones * 0.5):
        insight = "Aviso: Hay muchas sesiones sin reporte clínico. Los terapeutas deben ponerse al día."
    elif total_pacientes > 20:
        insight = "¡Felicidades! La clínica está creciendo. Considera agregar más caballos."

    return Response({
        "totalSesiones": total_sesiones,
        "totalPacientes": total_pacientes,
        "totalCaballos": total_caballos,
        "sesiones_hoy": sesiones_hoy,
        "expertos_hoy": expertos_hoy,
        "sesionesSemana": sesiones_por_dia,
        "crecimientoPacientes": pacientes_crecimiento,
        "usoCaballos": uso_caballos_list,
        "distribucionTerapeutas": dist_terapeutas_list,
        "salud": {
            "disponibilidad": disponibilidad_pct,
            "asistencia": asistencia_pct,
            "cumplimiento": cumplimiento_pct,
            "insight": insight
        }
    })

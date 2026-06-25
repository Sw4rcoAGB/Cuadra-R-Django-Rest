from rest_framework import serializers
from api.models import Caballo, BitacoraEquina
from api.common.utils import cap, cap_sentence

class CaballoSerializer(serializers.ModelSerializer):
    ultimo_evento = serializers.SerializerMethodField()
    sesiones_semana_actuales = serializers.SerializerMethodField()
    porcentaje_carga = serializers.SerializerMethodField()

    class Meta:
        model = Caballo
        fields = '__all__'
        depth = 1

    def get_ultimo_evento(self, obj):
        evento = obj.bitacoraequina_set.order_by('-fecha_evento', '-hora_evento', '-fecha_registro').first()
        if evento:
            return {
                "tipo": evento.tipo_evento.nombre,
                "descripcion": evento.descripcion_veterinaria,
                "fecha": evento.fecha_registro.strftime("%Y-%m-%d")
            }
        return None

    def get_sesiones_semana_actuales(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        hoy = timezone.now()
        inicio = hoy - timedelta(days=hoy.weekday())
        inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=7)
        return obj.sesion_set.filter(
            fecha_hora__gte=inicio,
            fecha_hora__lt=fin,
        ).exclude(estatus__nombre__in=['Cancelada']).count()

    def get_porcentaje_carga(self, obj):
        max_s = obj.sesiones_semanales_max or 10
        actual = self.get_sesiones_semana_actuales(obj)
        return round((actual / max_s) * 100, 1)

class CaballoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caballo
        fields = '__all__'

    def validate_nombre(self, v): return cap(v)
    def validate_raza(self, v):   return cap(v)
    def validate_tipo(self, v):   return cap(v)

class BitacoraEquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraEquina
        fields = '__all__'
        depth = 1

class BitacoraEquinaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraEquina
        fields = '__all__'

    def validate_descripcion_veterinaria(self, v): return cap_sentence(v)

from rest_framework import serializers
from api.models import Sesion, ReporteSesion, ReporteObjetivo

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'
        depth = 2

class SesionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'

    def validate(self, attrs):
        caballo = attrs.get('caballo')
        fecha_hora = attrs.get('fecha_hora')
        
        # Check if updating (self.instance exists)
        qs = Sesion.objects.filter(caballo=caballo, fecha_hora=fecha_hora).exclude(estatus__nombre='Cancelada')
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError({"caballo": "Este caballo ya tiene una sesión programada en esta fecha y hora."})
            
        return attrs

class ReporteSesionSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source='sesion.paciente.nombre', read_only=True, default='')
    caballo_nombre = serializers.CharField(source='sesion.caballo.nombre', read_only=True, default='')
    terapeuta_nombre = serializers.CharField(source='sesion.terapeuta.usuario.nombre_completo', read_only=True, default='')
    fecha_sesion = serializers.DateTimeField(source='sesion.fecha_hora', read_only=True)

    class Meta:
        model = ReporteSesion
        fields = '__all__'
        depth = 2

class ReporteSesionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSesion
        fields = '__all__'

class TutorReporteSesionSerializer(serializers.ModelSerializer):
    """Serializador para familias — solo campos visibles."""
    paciente_nombre = serializers.CharField(source='sesion.paciente.nombre', read_only=True, default='')
    caballo_nombre = serializers.CharField(source='sesion.caballo.nombre', read_only=True, default='')
    fecha_sesion = serializers.DateTimeField(source='sesion.fecha_hora', read_only=True)

    class Meta:
        model = ReporteSesion
        fields = ['id', 'sesion', 'paciente_nombre', 'caballo_nombre', 'fecha_sesion',
                  'ansiedad_inicial', 'ansiedad_final', 'recomendacion_casa']

class ReporteObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteObjetivo
        fields = '__all__'

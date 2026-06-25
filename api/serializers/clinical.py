from rest_framework import serializers
from api.models import Terapeuta, Paciente, PacienteDiagnostico, ContactoEmergencia
from api.common.utils import cap, cap_sentence

class TerapeutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terapeuta
        fields = '__all__'
        depth = 1

    def validate_nombre_completo(self, v): return cap(v)
    def validate_carrera(self, v): return cap(v)
    def validate_especialidad_text(self, v): return cap_sentence(v)
    def validate_contacto_emergencia(self, v): return cap(v)
    def validate_rfc(self, v): return v.upper() if v else v
    def validate_biografia(self, v): return cap_sentence(v)

class PacienteSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.nombre_completo', read_only=True)
    
    class Meta:
        model = Paciente
        fields = '__all__'
        depth = 1

    def validate_nombre(self, v):                  return cap(v)
    def validate_direccion(self, v):               return cap(v)
    def validate_ocupacion_escolaridad(self, v):   return cap_sentence(v)
    def validate_motivo_consulta(self, v):         return cap_sentence(v)
    def validate_historial_medico(self, v):        return cap_sentence(v)
    def validate_antecedentes_familiares(self, v): return cap_sentence(v)
    def validate_contacto_emergencia(self, v):     return cap(v)

class PacienteDiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteDiagnostico
        fields = '__all__'

class ContactoEmergenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactoEmergencia
        fields = '__all__'

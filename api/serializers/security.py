from rest_framework import serializers
from api.models import Usuario, BitacoraSeguridad
from api.common.utils import cap

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_nombre_completo(self, v): return cap(v)
    def validate_direccion(self, v):      return cap(v)

class BitacoraSeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraSeguridad
        fields = '__all__'
        depth = 1

from rest_framework import serializers
from api.models import (
    Rol, CatalogoEspecialidad, CatalogoDiagnostico, CatalogoObjetivo,
    CatalogoEstadoCaballo, CatalogoEventoEquino, CatalogoEstadoSesion,
    CatalogoEstadoPago, CatalogoParentesco
)

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class CatalogoEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEspecialidad
        fields = '__all__'

class CatalogoDiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDiagnostico
        fields = '__all__'

class CatalogoObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoObjetivo
        fields = '__all__'

class CatalogoEstadoCaballoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoCaballo
        fields = '__all__'

class CatalogoEventoEquinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEventoEquino
        fields = '__all__'

class CatalogoEstadoSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoSesion
        fields = '__all__'

class CatalogoEstadoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEstadoPago
        fields = '__all__'

class CatalogoParentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoParentesco
        fields = '__all__'

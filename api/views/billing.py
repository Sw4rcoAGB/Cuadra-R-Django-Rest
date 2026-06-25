from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.models import Pago
from api.serializers import PagoSerializer

@extend_schema_view(
    list=extend_schema(tags=['Pagos']),
    retrieve=extend_schema(tags=['Pagos']),
    create=extend_schema(tags=['Pagos']),
    update=extend_schema(tags=['Pagos']),
    partial_update=extend_schema(tags=['Pagos']),
    destroy=extend_schema(tags=['Pagos']),
)
class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

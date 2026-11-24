from django.db import transaction as db_transaction
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from repuestosApp.models import repuestos
from compraRepuestosApp.models import CompraRepuesto
from compraRepuestosApp.serializers import CompraRepuestoSerializer


def es_administrador(request):
    return request.user.groups.filter(name='Administrador').exists()


def cantidades_por_repuesto(detalles):
    cantidades = {}
    for detalle in detalles:
        cantidades[detalle.repuesto_id] = (
            cantidades.get(detalle.repuesto_id, 0) + detalle.cantidad
        )
    return cantidades


def ajustar_stock(antes, despues):
    repuesto_ids = set(antes) | set(despues)
    for repuesto_id in sorted(repuesto_ids):
        diferencia = (
            despues.get(repuesto_id, 0) - antes.get(repuesto_id, 0)
        )
        if diferencia:
            repuestos.objects.filter(pk=repuesto_id).update(
                stock=F('stock') + diferencia
            )


@extend_schema(
    description='Lista o crea compras de repuestos.',
    responses={
        200: CompraRepuestoSerializer(many=True),
        201: CompraRepuestoSerializer,
        400: OpenApiResponse(description='Datos inválidos'),
    },
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def compra_lista(request):
    if request.method == 'GET':
        compras = CompraRepuesto.objects.prefetch_related(
            'detalles_compra__repuesto'
        ).order_by('-fecha', '-pk')
        serializer = CompraRepuestoSerializer(compras, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not es_administrador(request):
            return Response(
                {'detalle': 'No tiene permisos para registrar compras.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CompraRepuestoSerializer(data=request.data)
        if serializer.is_valid():
            with db_transaction.atomic():
                compra = serializer.save()
                ajustar_stock({}, cantidades_por_repuesto(compra.detalles_compra.all()))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description='Consulta, actualiza o elimina una compra de repuestos.',
    responses={
        200: CompraRepuestoSerializer,
        204: OpenApiResponse(description='Compra eliminada'),
        404: OpenApiResponse(description='Compra no encontrada'),
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def compra_detalle(request, pk):
    try:
        compra = CompraRepuesto.objects.get(pk=pk)
    except CompraRepuesto.DoesNotExist:
        return Response(
            {'detalle': 'Compra no encontrada.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = CompraRepuestoSerializer(compra)
        return Response(serializer.data)

    if not es_administrador(request):
        return Response(
            {'detalle': 'No tiene permisos para modificar o eliminar compras.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'PUT':
        serializer = CompraRepuestoSerializer(compra, data=request.data, partial=True)
        if serializer.is_valid():
            with db_transaction.atomic():
                antes = cantidades_por_repuesto(compra.detalles_compra.all())
                serializer.save()
                despues = cantidades_por_repuesto(compra.detalles_compra.all())
                ajustar_stock(antes, despues)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        with db_transaction.atomic():
            antes = cantidades_por_repuesto(compra.detalles_compra.all())
            compra.delete()
            ajustar_stock(antes, {})
        return Response(status=status.HTTP_204_NO_CONTENT)

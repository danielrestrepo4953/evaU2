from repuestosApi.serializer import RepuestoAdminSerializer, RepuestoPublicSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from repuestosApp.models import repuestos as Repuesto
from drf_spectacular.utils import extend_schema, OpenApiResponse


def obtener_serializer(user):
    if user.groups.filter(name='Administrador').exists():
        return RepuestoAdminSerializer
    return RepuestoPublicSerializer


def es_administrador(request):
    return request.user.groups.filter(name='Administrador').exists()


@extend_schema(
    description='Lista los repuestos según el rol del usuario.',
    responses={200: RepuestoPublicSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def repuestos(request):
    repuestos_lista = Repuesto.objects.all()
    serializer_clase = obtener_serializer(request.user)
    serializer = serializer_clase(repuestos_lista, many=True)
    return Response({'repuestos': serializer.data})


@extend_schema(
    description='Lista o crea repuestos.',
    responses={
        200: RepuestoPublicSerializer(many=True),
        201: RepuestoAdminSerializer,
        400: OpenApiResponse(description='Datos inválidos'),
    },
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def repuesto_lista(request):
    if request.method == 'GET':
        repuestos_lista = Repuesto.objects.all()
        serializer_clase = obtener_serializer(request.user)
        serializer = serializer_clase(repuestos_lista, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not es_administrador(request):
            return Response(
                {'detalle': 'No tiene permisos para crear repuestos.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RepuestoAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description='Consulta, actualiza o elimina un repuesto por id.',
    responses={
        200: RepuestoPublicSerializer,
        204: OpenApiResponse(description='Repuesto eliminado'),
        404: OpenApiResponse(description='Repuesto no encontrado'),
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def repuesto_detalle(request, pk):
    try:
        repuesto = Repuesto.objects.get(id=pk)
    except Repuesto.DoesNotExist:
        return Response(
            {'detalle': 'Repuesto no encontrado.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer_clase = obtener_serializer(request.user)
        serializer = serializer_clase(repuesto)
        return Response(serializer.data)

    if not es_administrador(request):
        return Response(
            {'detalle': 'No tiene permisos para modificar o eliminar repuestos.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'PUT':
        serializer = RepuestoAdminSerializer(repuesto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        repuesto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from empleadosApp.models import Empleado
from empleadosApp.serializers import EmpleadoAdminSerializer, EmpleadoPublicSerializer


def obtener_serializer(user):
    if user.groups.filter(name='Administrador').exists():
        return EmpleadoAdminSerializer
    return EmpleadoPublicSerializer


def es_administrador(request):
    return request.user.groups.filter(name='Administrador').exists()


@extend_schema(
    description='Lista o crea empleados.',
    responses={
        200: EmpleadoPublicSerializer(many=True),
        201: EmpleadoAdminSerializer,
        400: OpenApiResponse(description='Datos inválidos'),
    },
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def empleado_lista(request):
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        serializer_clase = obtener_serializer(request.user)
        serializer = serializer_clase(empleados, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not es_administrador(request):
            return Response(
                {'detalle': 'No tiene permisos para crear empleados.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EmpleadoAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description='Consulta, actualiza o elimina un empleado.',
    responses={
        200: EmpleadoPublicSerializer,
        204: OpenApiResponse(description='Empleado eliminado'),
        404: OpenApiResponse(description='Empleado no encontrado'),
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def empleado_detalle(request, pk):
    try:
        empleado = Empleado.objects.get(id=pk)
    except Empleado.DoesNotExist:
        return Response(
            {'detalle': 'Empleado no encontrado.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer_clase = obtener_serializer(request.user)
        serializer = serializer_clase(empleado)
        return Response(serializer.data)

    if not es_administrador(request):
        return Response(
            {'detalle': 'No tiene permisos para modificar o eliminar empleados.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'PUT':
        serializer = EmpleadoAdminSerializer(empleado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        empleado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

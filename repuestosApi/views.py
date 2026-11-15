from django.shortcuts import render
from repuestosApi.serializer import RepuestoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from repuestosApp.models import repuestos as Repuesto


def repuestos(request):
    datos = Repuesto.objects.all().values(
        'codigo',
        'nombre',
        'detalle',
        'precio',
        'stock',
    )
    return JsonResponse({'repuestos': list(datos)})

@api_view(['GET', 'POST'])
def repuesto_lista(request):
    if request.method == 'GET':
        repuestos = Repuesto.objects.all()
        serializer = RepuestoSerializer(repuestos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RepuestoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def repuesto_detalle(request, pk):
    try:
        repuesto = Repuesto.objects.get(id=pk)
    except Repuesto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RepuestoSerializer(repuesto)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RepuestoSerializer(repuesto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        repuesto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
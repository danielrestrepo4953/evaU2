from django.shortcuts import render
import json
import os
# Create your views here.
def cargar_empleados():
    ruta = os.path.join(os.path.dirname(__file__), 'empleados.json')

    with open(ruta, encoding='utf-8') as archivo:
        empleados = json.load(archivo)

    return empleados

def principal(request):
    empleados = cargar_empleados()
    datos = {
        'empleados': empleados
    }

    return render(request, 'empleados/lista.html', datos)

def detalle(request, id):
    empleados = cargar_empleados()
    empleado = None
    for emp in empleados:
        if emp['id'] == id:
            empleado = emp
            break

    return render(request, 'empleados/detalle.html', {"empleado": empleado})

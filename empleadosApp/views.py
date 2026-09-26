from django.shortcuts import render
from empleadosApp.models import Empleado

# Create your views here.
def principal(request):
    empleados = Empleado.objects.all()
    datos = {
        'empleados': empleados
    }
    return render(request, 'empleados/lista.html', datos)

def detalle(request, id):
    empleado = Empleado.objects.filter(id=id).first()
    return render(request, 'empleados/detalle.html', {"empleado": empleado})

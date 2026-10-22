from django.shortcuts import render
from empleadosApp.models import Empleado
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def principal(request):
    empleados = Empleado.objects.all()
    datos = {
        'empleados': empleados
    }
    return render(request, 'empleados/lista.html', datos)

@login_required
def detalle(request, id):
    empleado = Empleado.objects.filter(id=id).first()
    return render(request, 'empleados/detalle.html', {"empleado": empleado})

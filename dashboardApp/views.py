from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from vehiculosApp.models import Vehiculo, Detalle
from repuestosApp.models import repuestos
from empleadosApp.models import Empleado
from clientesApp.models import Cliente
from reparacionesApp.models import Reparacion 
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect




@login_required
def redireccionar_por_grupo(request):
    usuario = request.user

    if usuario.groups.filter(name="Administrador").exists():
        return redirect("dashboard_admin")

    if usuario.groups.filter(name="Supervisor").exists():
        return redirect("dashboard_supervisor")

    if usuario.groups.filter(name="Empleado").exists():
        return redirect("dashboard_empleado")

    return redirect("menu-principal")


@login_required
def cargar_dashboard_empleado(request):
    if not request.user.groups.filter(name="Empleado"):
            return redirect('redireccionar_usuario')
    contexto = {
        'total_vehiculos' : Vehiculo.objects.count(),
        'vehiculos_mal_estado' : Detalle.objects.filter(estado = 'Malas').count(),
        'total_repuestos' : repuestos.objects.count(),
        'total_empleados' : Empleado.objects.count(),
        'total_clientes' : Cliente.objects.count()
    }

    return render(request, 'dashboards/dashboard_empleados.html', contexto)

@login_required
def cargar_dashboard_supervisor(request):

    if not request.user.groups.filter(name="Supervisor"):
            return redirect('redireccionar_usuario')
    contexto = {
        'total_vehiculos' : Vehiculo.objects.count(),
        'vehiculos_mal_estado' : Detalle.objects.filter(estado = 'Malas').count(),
        'total_repuestos' : repuestos.objects.count(),
        'total_empleados' : Empleado.objects.count(),
        'total_clientes' : Cliente.objects.count(),
        'total_reparaciones' : Reparacion.objects.count()
    }

    return render(request, 'dashboards/dashboard_supervisor.html', contexto)

@login_required
def cargar_dashboard_administrador(request):

    if not request.user.groups.filter(name="Administrador"):
        return redirect('redireccionar_usuario')

    User= get_user_model()
    total_usuarios = User.objects.count()
    contexto = {
        'total_vehiculos' : Vehiculo.objects.count(),
        'vehiculos_mal_estado' : Detalle.objects.filter(estado = 'Malas').count(),
        'total_repuestos' : repuestos.objects.count(),
        'total_empleados' : Empleado.objects.count(),
        'total_clientes' : Cliente.objects.count(),
        'total_reparaciones' : Reparacion.objects.count(),
        'total_usuarios' : total_usuarios
    }

    return render(request, 'dashboards/dashboard_administrador.html', contexto)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from clientesVehiculosApp.models import ClienteVehiculo
from clientesVehiculosApp.forms import ClienteVehiculoForm

@login_required
@permission_required('clientesVehiculosApp.view_clientevehiculo', raise_exception=True)
def lista_clientes_vehiculos(request):
    asociaciones = ClienteVehiculo.objects.select_related('cliente', 'vehiculo').all()
    return render(request, 'clientes_vehiculos/lista.html', {'asociaciones': asociaciones})

@login_required
@permission_required('clientesVehiculosApp.add_clientevehiculo', raise_exception=True)
def asociar_cliente_vehiculo(request):
    if request.method == 'POST':
        form = ClienteVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes_vehiculos')
    else:
        form = ClienteVehiculoForm()
    
    return render(request, 'clientes_vehiculos/formulario.html', {'form': form})

@login_required
@permission_required('clientesVehiculosApp.change_clientevehiculo', raise_exception=True)
def editar_asociacion(request, asociacion_id):
    asociacion = get_object_or_404(ClienteVehiculo, id=asociacion_id)
    if request.method == 'POST':
        form = ClienteVehiculoForm(request.POST, instance=asociacion)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes_vehiculos')
    else:
        form = ClienteVehiculoForm(instance=asociacion)
    
    return render(request, 'clientes_vehiculos/formulario.html', {'form': form, 'es_edicion': True})

@login_required
@permission_required('clientesVehiculosApp.delete_clientevehiculo', raise_exception=True)
def eliminar_asociacion(request, asociacion_id):
    asociacion = get_object_or_404(ClienteVehiculo, id=asociacion_id)
    if request.method == 'POST':
        asociacion.delete()
        return redirect('lista_clientes_vehiculos')
    return render(request, 'clientes_vehiculos/eliminar.html', {'asociacion': asociacion})
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Q, Value, ProtectedError, RestrictedError
from django.db.models.functions import Replace
from django.shortcuts import render, redirect, get_object_or_404

from empleadosApp.forms import EmpleadoForm, DetalleEmpleadoForm
from empleadosApp.models import Empleado, DetalleEmpleado


# Create your views here.
@login_required
@permission_required('empleadosApp.view_empleado', raise_exception=True)
def principal(request):
    busqueda = request.GET.get('q', '').strip()
    # El RUT se compara sin puntos para encontrarlo escrito de cualquier forma
    empleados = (Empleado.objects
                 .select_related('detalle')
                 .annotate(rut_sin_puntos=Replace('rut', Value('.'), Value(''))))

    # Cada palabra debe coincidir con algún campo, así "Luis Diaz" encuentra nombre + apellido
    for palabra in busqueda.split():
        empleados = empleados.filter(
            Q(rut_sin_puntos__icontains=palabra.replace('.', '')) |
            Q(nombre__icontains=palabra) |
            Q(apellido__icontains=palabra) |
            Q(cargo__icontains=palabra)
        )

    datos = {
        'empleados': empleados,
        'busqueda': busqueda,
    }
    return render(request, 'empleados/lista.html', datos)


@login_required
@permission_required('empleadosApp.view_empleado', raise_exception=True)
def detalle(request, id):
    empleado = get_object_or_404(Empleado.objects.select_related('detalle'), id=id)
    return render(request, 'empleados/detalle.html', {"empleado": empleado})


@login_required
@permission_required('empleadosApp.add_empleado', raise_exception=True)
@permission_required('empleadosApp.add_detalleempleado', raise_exception=True)
def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        detalle_form = DetalleEmpleadoForm(request.POST, request.FILES)

        if form.is_valid() and detalle_form.is_valid():
            with transaction.atomic():
                empleado = form.save()
                detalle = detalle_form.save(commit=False)
                detalle.empleado = empleado
                detalle.save()
            messages.success(request, 'Se registró el empleado correctamente.')
            return redirect('principal')
    else:
        form = EmpleadoForm()
        detalle_form = DetalleEmpleadoForm()

    return render(request, 'empleados/formulario.html', {
        'form': form,
        'detalle_form': detalle_form,
    })


@login_required
@permission_required('empleadosApp.change_empleado', raise_exception=True)
@permission_required('empleadosApp.change_detalleempleado', raise_exception=True)
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    # Algunos empleados antiguos pueden no tener detalle; en ese caso se crea al guardar
    detalle = DetalleEmpleado.objects.filter(empleado=empleado).first() or DetalleEmpleado(empleado=empleado)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        detalle_form = DetalleEmpleadoForm(request.POST, request.FILES, instance=detalle)

        if form.is_valid() and detalle_form.is_valid():
            with transaction.atomic():
                form.save()
                detalle_form.save()
            messages.success(request, 'El empleado fue editado correctamente.')
            return redirect('principal')
    else:
        form = EmpleadoForm(instance=empleado)
        detalle_form = DetalleEmpleadoForm(instance=detalle)

    return render(request, 'empleados/formulario.html', {
        'form': form,
        'detalle_form': detalle_form,
        'empleado': empleado,
    })


@login_required
@permission_required('empleadosApp.delete_empleado', raise_exception=True)
@permission_required('empleadosApp.delete_detalleempleado', raise_exception=True)
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if request.method == 'POST':
        try:
            empleado.delete()
        except (ProtectedError, RestrictedError):
            messages.warning(request,'No se puede eliminar el empleado porque tiene asignaciones de vehículos '
                                    'registradas. Elimina primero sus asignaciones.')
            return redirect('principal')

        messages.success(request, 'El empleado se ha eliminado correctamente.')
        return redirect('principal')

    return render(request, 'empleados/eliminar.html', {'empleado': empleado})

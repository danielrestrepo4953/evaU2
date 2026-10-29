from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from asignacionesApp.models import Asignacion
from asignacionesApp.forms import AsignacionForm


# Create your views here.
@login_required
@permission_required('asignacionesApp.view_asignacion', raise_exception=True)
def inicio_asignaciones(request):
    busqueda = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    asignaciones = Asignacion.objects.select_related('empleado', 'vehiculo')

    if busqueda:
        asignaciones = asignaciones.filter(
            Q(empleado__nombre__icontains=busqueda) |
            Q(empleado__apellido__icontains=busqueda) |
            Q(empleado__rut__icontains=busqueda) |
            Q(vehiculo__marca__icontains=busqueda) |
            Q(vehiculo__modelo__icontains=busqueda) |
            Q(vehiculo__patente__icontains=busqueda) |
            Q(motivo__icontains=busqueda)
        )

    if estado in (Asignacion.ACTIVA, Asignacion.FINALIZADA):
        asignaciones = asignaciones.filter(estado=estado)

    datos = {
        'asignaciones': asignaciones,
        'busqueda': busqueda,
        'estado': estado,
        'estados': Asignacion.ESTADOS,
    }
    return render(request, 'asignaciones/inicio.html', datos)


@login_required
@permission_required('asignacionesApp.add_asignacion', raise_exception=True)
def registrar_asignacion(request):
    if request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se registró la asignación correctamente.')
            return redirect('inicio_asignaciones')
    else:
        form = AsignacionForm()

    return render(request, 'asignaciones/formulario.html', {'form': form})


@login_required
@permission_required('asignacionesApp.change_asignacion', raise_exception=True)
def editar_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'La asignación fue editada correctamente.')
            return redirect('inicio_asignaciones')
    else:
        form = AsignacionForm(instance=asignacion)

    return render(request, 'asignaciones/formulario.html', {
        'form': form,
        'asignacion': asignacion,
    })


@login_required
@permission_required('asignacionesApp.delete_asignacion', raise_exception=True)
def eliminar_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(Asignacion, id=asignacion_id)

    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'La asignación se ha eliminado correctamente.')
        return redirect('inicio_asignaciones')

    return render(request, 'asignaciones/eliminar.html', {'asignacion': asignacion})

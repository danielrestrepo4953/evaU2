from django.shortcuts import render, redirect, get_object_or_404
from reparacionesApp.models import Reparacion, RepuestoUtilizado
from vehiculosApp.models import Vehiculo
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from reparacionesApp.forms import ReparacionForm, RepuestoUtilizadoFormSet
from repuestosApp.models import repuestos

# Create your views here.
@login_required
@permission_required('reparacionesApp.view_reparacion', raise_exception=True)
@permission_required('reparacionesApp.view_repuestoutilizado', raise_exception=True)
def principal_reparaciones(request):
    reparaciones = Reparacion.objects.all()
# vehiculo = next((v for v in vehiculos if v.get('id') == reparaciones.vehiculo_id), None)


    datos = {
        'reparaciones': reparaciones,

    }
    return render(request, 'reparaciones/inicio.html', datos)

@login_required
@permission_required('reparacionesApp.add_reparacion', raise_exception=True)
@permission_required('reparacionesApp.add_repuestoutilizado', raise_exception=True)
def registrar_reparacion(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        formset = RepuestoUtilizadoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                reparacion = form.save()

                formset.instance = reparacion 
                formset.save()
            messages.success(request, 'Se registró la reparación correctamente.')
            return redirect('inicio_reparaciones')

    else:
        form = ReparacionForm()
        formset = RepuestoUtilizadoFormSet()

    contexto = {
        'form' : form,
        'formset' : formset,
        }

    
    return render(request, 'reparaciones/formulario.html', contexto)

@login_required
@permission_required('reparacionesApp.change_reparacion', raise_exception=True)
@permission_required('reparacionesApp.change_repuestoutilizado', raise_exception=True)
def cargar_editar_reparacion(request, reparacion_id):

    reparacion= get_object_or_404(Reparacion, id= reparacion_id)
    form = ReparacionForm(instance=reparacion)
    formset = RepuestoUtilizadoFormSet(instance=reparacion)

    contexto = {
        'form' : form,
        'formset' : formset,
        'reparacion' : reparacion
    }

    return render (request, 'reparaciones/formulario.html',
                   contexto)

@login_required
@permission_required('reparacionesApp.change_reparacion', raise_exception=True)
@permission_required('reparacionesApp.change_repuestoutilizado', raise_exception=True)
def editar_reparacion(request, reparacion_id):
    reparacion = get_object_or_404(Reparacion, id= reparacion_id)

    if request.method == 'POST':
        form = ReparacionForm(request.POST, instance=reparacion)
        formset = RepuestoUtilizadoFormSet(request.POST, instance= reparacion)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                reparacion = form.save()
                
                formset.instance = reparacion 
                formset.save()

            messages.success(request, 'La reparación fue editada correctamente.')    
            return redirect('inicio_reparaciones')

@login_required
@permission_required('reparacionesApp.delete_reparacion', raise_exception=True)
@permission_required('reparacionesApp.delete_repuestoutilizado', raise_exception=True)
def eliminar_reparacion(request, reparacion_id):
    reparacion= get_object_or_404(Reparacion, id= reparacion_id)

    if request.method == 'POST':
        reparacion.delete()
        messages.success(request, 'La reparación se ha eliminado correctamente')
        return redirect('inicio_reparaciones')

    return render(request, 'reparaciones/eliminar.html', {'reparacion' : reparacion})
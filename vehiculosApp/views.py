from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
import json
from pathlib import Path
from vehiculosApp.models import Vehiculo, Detalle
from vehiculosApp.forms import VehiculoForm, DetalleForm, detalle_formset

# Create your views here.
@login_required
def menu_principal(request):
    return render(request, 'principal.html')


@login_required
@permission_required('vehiculosApp.view_vehiculo', raise_exception=True)
def inicio_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/inicio.html', {'vehiculos': vehiculos})

@login_required
@permission_required('vehiculosApp.view_detalle', raise_exception=True)
def detalle_vehiculo(request, vehiculo_id):
    

    vehiculos = Vehiculo.objects.all().values()
    detalles = Detalle.objects.all().values()

    vehiculo = next((v for v in vehiculos if v.get('id') == vehiculo_id), None)
    detalle = next((d for d in detalles if d.get('vehiculo_id') == vehiculo_id), None)

    return render(request, 'vehiculos/detalle.html', {
        'vehiculo': vehiculo,
        'detalle': detalle,
    })

@login_required
@permission_required('vehiculosApp.add_vehiculo', raise_exception=True)
@permission_required('vehiculosApp.add_detalle', raise_exception=True)
def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        formset = detalle_formset(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                vehiculo = form.save()

                formset.instance = vehiculo
                formset.save()
            messages.success(request, 'Se registró el vehiculo correctamente.')
            return redirect('inicio-vehiculos')

    else:
        form = VehiculoForm()
        formset = detalle_formset()

    contexto = {
        'form' : form,
        'formset' : formset,
        }

    return render(request, 'vehiculos/formulario.html', contexto)

@login_required
@permission_required('vehiculosApp.change_vehiculo', raise_exception=True)
@permission_required('vehiculosApp.change_detalle', raise_exception=True)
def cargar_editar_vehiculo(request, vehiculo_id):

    vehiculo= get_object_or_404(Vehiculo, id= vehiculo_id)
    form = VehiculoForm(instance=vehiculo)
    formset = detalle_formset(instance=vehiculo)

    contexto = {
        'form' : form,
        'formset' : formset,
        'vehiculo' : vehiculo
    }

    return render (request, 'vehiculos/formulario.html',
                   contexto)

@login_required
@permission_required('vehiculosApp.change_vehiculo', raise_exception=True)
@permission_required('vehiculosApp.change_detalle', raise_exception=True)
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id= vehiculo_id)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        formset = detalle_formset(request.POST, instance= vehiculo)

        if form.is_valid() and formset.is_valid():
            if 'imagen' in request.FILES:
                vehiculo.imagen = request.FILES['imagen']
            with transaction.atomic():
                vehiculo = form.save()
                formset.instance = vehiculo 
                formset.save()

            messages.success(request, 'El vehículo fue editado correctamente.')    
            return redirect('inicio-vehiculos')

        return render(request, 'vehiculos/formulario.html', {
    'form': form,
    'formset': formset,
    'vehiculo': vehiculo,
})

@permission_required('vehiculosApp.delete_vehiculo', raise_exception=True)
@permission_required('vehiculosApp.delete_detalle', raise_exception=True)
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo= get_object_or_404(Vehiculo, id= vehiculo_id)
    detalle = get_object_or_404(Detalle, vehiculo=vehiculo)

    if request.method == 'POST':
        vehiculo.delete()
        detalle.delete()
        messages.success(request, 'El vehículo se ha eliminado correctamente')
        return redirect('inicio-vehiculos')

    return render(request, 'vehiculos/eliminar.html', {'vehiculo' : vehiculo})

from django.shortcuts import render, redirect, get_object_or_404
from reparacionesApp.models import Reparacion, RepuestoUtilizado
from vehiculosApp.models import Vehiculo
from django.contrib.auth.decorators import login_required
from django.db import transaction
from reparacionesApp.forms import ReparacionForm, RepuestoUtilizadoFormSet
from repuestosApp.models import repuestos

# Create your views here.
@login_required
def principal_reparaciones(request):
    reparaciones = Reparacion.objects.all()
# vehiculo = next((v for v in vehiculos if v.get('id') == reparaciones.vehiculo_id), None)


    datos = {
        'reparaciones': reparaciones,

    }
    return render(request, 'reparaciones/inicio.html', datos)

@login_required
def registrar_reparacion(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        formset = RepuestoUtilizadoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                reparacion = form.save()

                formset.instance = reparacion 
                formset.save()

            return redirect('inicio_reparaciones')

    else:
        form = ReparacionForm()
        formset = RepuestoUtilizadoFormSet()

    contexto = {
        'form' : form,
        'formset' : formset,
        }

    return render(request, 'reparaciones/formulario.html', contexto)


def cargar_editar_reparacion(request, reparacion_id):

    reparacion= get_object_or_404(Reparacion, id= reparacion_id)
    form = ReparacionForm(instance=reparacion)
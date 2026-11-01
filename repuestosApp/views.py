from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from repuestosApp.models import repuestos, descripcion
from .forms import RepuestoForm

@login_required
def inicio(request):
    repuesto = repuestos.objects.all()
    return render(request, 'repuestos/repuestos/inicio.html', {'repuestos': repuesto})

@login_required
def detalle_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    detalle = descripcion.objects.filter(repuesto_id=repuesto_id).first()
    return render(
        request,
        'repuestos/repuestos/usuario.html',
        {'repuesto': repuesto, 'detalle': detalle}
    )


@login_required
def crear_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El repuesto se registró correctamente.')
            return redirect('home_repuestos')
    else:
        form = RepuestoForm()

    return render(request, 'repuestos/repuestos/formulario.html', {'form': form})


@login_required
def editar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, 'El repuesto se actualizó correctamente.')
            return redirect('home_repuestos')
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'repuestos/repuestos/formulario.html', {
        'form': form,
        'repuesto': repuesto,
    })


@login_required
def eliminar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    if request.method == 'POST':
        repuesto.delete()
        messages.success(request, 'El repuesto se eliminó correctamente.')
        return redirect('home_repuestos')

    return render(request, 'repuestos/repuestos/eliminar.html', {'repuesto': repuesto})

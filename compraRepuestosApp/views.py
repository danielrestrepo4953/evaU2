from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from repuestosApp.models import repuestos
from compraRepuestosApp.models import CompraRepuesto, DetalleCompra
from compraRepuestosApp.forms import CompraRepuestoForm, DetalleCompraFormSet


@login_required
@permission_required('compraRepuestosApp.view_comprarepuesto', raise_exception=True)
def principal_ventas(request):
    compras = CompraRepuesto.objects.select_related('cliente').prefetch_related(
        'detalles_compra__repuesto'
    ).order_by('-fecha', '-pk')
    return render(request, 'compras/inicio.html', {'compras': compras})


@login_required
@permission_required(('compraRepuestosApp.view_comprarepuesto',
                      'compraRepuestosApp.add_comprarepuesto',
                      'compraRepuestosApp.add_detallecompra'), raise_exception=True)
def registrar_compra(request):
    if request.method == 'POST':
        form = CompraRepuestoForm(request.POST)
        formset = DetalleCompraFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                compra = form.save()

                formset.instance = compra
                detalles = formset.save()
                # La suma se hace en la base de datos para conservar compras simultaneas.
                for detalle in sorted(detalles, key=lambda item: item.repuesto_id):
                    repuestos.objects.filter(pk=detalle.repuesto_id).update(
                        stock=F('stock') + detalle.cantidad
                    )

            return redirect('inicio_compras')

    else:
        form = CompraRepuestoForm()
        formset = DetalleCompraFormSet()

    contexto = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'compras/formulario.html', contexto)


def _cantidades_por_repuesto(detalles):
    cantidades = {}
    for detalle in detalles:
        cantidades[detalle.repuesto_id] = (
            cantidades.get(detalle.repuesto_id, 0) + detalle.cantidad
        )
    return cantidades


def _actualizar_stock(cantidades_anteriores, cantidades_nuevas):
    repuesto_ids = set(cantidades_anteriores) | set(cantidades_nuevas)
    for repuesto_id in sorted(repuesto_ids):
        diferencia = (
            cantidades_nuevas.get(repuesto_id, 0)
            - cantidades_anteriores.get(repuesto_id, 0)
        )
        if diferencia:
            repuestos.objects.filter(pk=repuesto_id).update(
                stock=F('stock') + diferencia
            )


@login_required
@permission_required(
    ('compraRepuestosApp.view_comprarepuesto',
     'compraRepuestosApp.change_comprarepuesto',
     'compraRepuestosApp.change_detallecompra'),
    raise_exception=True,
)
def editar_compra(request, compra_id):
    compra = get_object_or_404(
        CompraRepuesto.objects.prefetch_related('detalles_compra'),
        pk=compra_id,
    )

    if request.method == 'POST':
        form = CompraRepuestoForm(request.POST, instance=compra)
        formset = DetalleCompraFormSet(request.POST, instance=compra)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                compra = CompraRepuesto.objects.select_for_update().get(
                    pk=compra.pk
                )
                detalles_anteriores = list(
                    DetalleCompra.objects.filter(compra=compra)
                )
                cantidades_anteriores = _cantidades_por_repuesto(
                    detalles_anteriores
                )
                cantidades_nuevas = _cantidades_por_repuesto(
                    DetalleCompra(
                        repuesto_id=detalle_form.cleaned_data['repuesto'].pk,
                        cantidad=detalle_form.cleaned_data['cantidad'],
                    )
                    for detalle_form in formset
                    if detalle_form.cleaned_data
                    and not detalle_form.cleaned_data.get('DELETE', False)
                )

                repuesto_ids = (
                    set(cantidades_anteriores) | set(cantidades_nuevas)
                )
                list(
                    repuestos.objects.select_for_update().filter(
                        pk__in=repuesto_ids
                    )
                )
                form.save()
                formset.instance = compra
                formset.save()
                detalles_nuevos = DetalleCompra.objects.filter(compra=compra)
                _actualizar_stock(
                    cantidades_anteriores,
                    _cantidades_por_repuesto(detalles_nuevos),
                )

            messages.success(request, 'La compra fue editada correctamente.')
            return redirect('inicio_compras')
    else:
        form = CompraRepuestoForm(instance=compra)
        formset = DetalleCompraFormSet(instance=compra)

    return render(request, 'compras/formulario.html', {
        'form': form,
        'formset': formset,
        'compra': compra,
    })


@login_required
@permission_required(
    ('compraRepuestosApp.delete_comprarepuesto',
     'compraRepuestosApp.delete_detallecompra'),
    raise_exception=True,
)
def eliminar_compra(request, compra_id):
    compra = get_object_or_404(
        CompraRepuesto.objects.prefetch_related('detalles_compra'),
        pk=compra_id,
    )

    if request.method == 'POST':
        with transaction.atomic():
            compra = CompraRepuesto.objects.select_for_update().get(
                pk=compra.pk
            )
            detalles = list(compra.detalles_compra.all())
            cantidades = _cantidades_por_repuesto(detalles)
            list(
                repuestos.objects.select_for_update().filter(
                    pk__in=cantidades
                )
            )
            compra.delete()
            _actualizar_stock(cantidades, {})

        messages.success(request, 'La compra se ha eliminado correctamente.')
        return redirect('inicio_compras')

    return render(request, 'compras/eliminar.html', {'compra': compra})

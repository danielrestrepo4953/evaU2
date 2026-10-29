from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import F
from repuestosApp.models import repuestos
from compraRepuestosApp.models import CompraRepuesto
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

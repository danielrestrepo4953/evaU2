from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ClienteForm

@login_required
@permission_required('clientesApp.view_cliente', raise_exception=True)
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

@login_required
@permission_required('clientesApp.view_cliente', raise_exception=True)
def detalle_cliente(request, nombre):
    cliente = get_object_or_404(Cliente, nombre__iexact=nombre)
    contexto = {
        'nombre': cliente.nombre,
        'apellido': cliente.apellido,
        'correo': cliente.correo,
        'cargo': cliente.cargo,
        'telefono': cliente.telefono,
        'direccion': cliente.direccion,
        'saldo': cliente.saldo,
        'imagen': cliente.imagen,
    }
    return render(request, 'clientes/detalle_cliente.html', contexto)

@login_required
@permission_required('clientesApp.add_cliente', raise_exception=True)
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

@login_required
@permission_required('clientesApp.change_cliente', raise_exception=True)
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('home_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
@permission_required('clientesApp.delete_cliente', raise_exception=True)
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('home_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})
from django.shortcuts import render, get_object_or_404
from .models import Cliente

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

def detalle_cliente(request, nombre):
    cliente = get_object_or_404(Cliente, nombre__iexact=nombre)
    
    # Preparamos las variables con los datos del cliente para que coincidan con tu HTML actual
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
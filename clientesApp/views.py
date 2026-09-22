from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import json

def lista_clientes(request):
    json_path = Path(settings.BASE_DIR) / 'clientesApp' / 'data' / 'clientes.json'
    
    with open(json_path, encoding='utf-8') as file:
        clientes = json.load(file)
        
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

def detalle_cliente(request, nombre):
    json_path = Path(settings.BASE_DIR) / 'clientesApp' / 'data' / 'clientes.json'
    
    with open(json_path, encoding='utf-8') as file:
        clientes = json.load(file)
    
    cliente_encontrado = None
    for c in clientes:
        if c['nombre'].lower() == nombre.lower():
            cliente_encontrado = c
            break

    return render(request, 'clientes/detalle_cliente.html', cliente_encontrado)
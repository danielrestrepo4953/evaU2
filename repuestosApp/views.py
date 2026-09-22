from django.shortcuts import render
import json
from pathlib import Path
from django.conf import settings


def inicio(request):
    """Vista que muestra la lista de repuestos desde JSON"""
    ruta_json = Path(settings.BASE_DIR) / 'repuestosApp' / 'json' / 'repuestos.json'

    with open(ruta_json, encoding='utf-8') as archivo:
        repuestos = json.load(archivo)

    contexto = {
        'repuestos': repuestos
    }

    return render(request, 'repuestos/repuestos/inicio.html', contexto)


def detalle_repuesto(request, repuesto_id):
    """Vista que muestra los detalles de un repuesto específico"""
    ruta_json = Path(settings.BASE_DIR) / 'repuestosApp' / 'json' / 'repuestos.json'

    with open(ruta_json, encoding='utf-8') as archivo:
        repuestos = json.load(archivo)

    # Buscar el repuesto por ID
    repuesto = None
    for item in repuestos:
        if item['id'] == repuesto_id:
            repuesto = item
            break

    if not repuesto:
        repuesto = repuestos[0]  # Mostrar el primero si no encuentra

    return render(
        request,
        'repuestos/repuestos/usuario.html',
        {'repuesto': repuesto}
    )

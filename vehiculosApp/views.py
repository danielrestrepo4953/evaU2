from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
from pathlib import Path

# Create your views here.
def menu_principal(request):
    return render(request, 'principal.html')

def inicio_vehiculos(request):
    json_path = Path(settings.BASE_DIR) / 'vehiculosApp' / 'datos JSON' / 'data.json'
    with open(json_path, encoding='utf-8') as file:
        data = json.load(file)

    vehiculos = data.get('vehiculos', [])
    return render(request, 'vehiculos/inicio.html', {'vehiculos': vehiculos})

def detalle_vehiculo(request, vehiculo_id):
    json_path = Path(settings.BASE_DIR) / 'vehiculosApp' / 'datos JSON' / 'data.json'

    with open(json_path, encoding='utf-8') as file:
        data = json.load(file)

    vehiculos = data.get('vehiculos', [])
    detalles = data.get('detalles', [])

    vehiculo = next((v for v in vehiculos if v.get('id') == vehiculo_id), None)
    detalle = next((d for d in detalles if d.get('id') == vehiculo_id), None)

    return render(request, 'vehiculos/detalle.html', {
        'vehiculo': vehiculo,
        'detalle': detalle,
    })

        

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
from pathlib import Path
from vehiculosApp.models import Vehiculo, Detalle

# Create your views here.
def menu_principal(request):
    return render(request, 'principal.html')

def inicio_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/inicio.html', {'vehiculos': vehiculos})

def detalle_vehiculo(request, vehiculo_id):
    

    vehiculos = Vehiculo.objects.all().values()
    detalles = Detalle.objects.all().values()

    vehiculo = next((v for v in vehiculos if v.get('id') == vehiculo_id), None)
    detalle = next((d for d in detalles if d.get('vehiculo_id') == vehiculo_id), None)

    return render(request, 'vehiculos/detalle.html', {
        'vehiculo': vehiculo,
        'detalle': detalle,
    })

        

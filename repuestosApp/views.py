from django.shortcuts import get_object_or_404, render
from repuestosApp.models import repuestos, descripcion
from django.contrib.auth.decorators import login_required

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

from django.contrib import admin
from vehiculosApp.models import Vehiculo, Detalle
# Register your models here.
class vehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'anio', 'patente')
    search_fields = ('marca', 'modelo', 'patente')
    list_filter = ('anio',)

class detalleAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'color', 'tipo_motor', 'tipo_caja', 'fecha_ultimo_servicio', 'kilometraje', 'estado')
    search_fields = ('vehiculo__marca', 'vehiculo__modelo', 'color', 'tipo_motor', 'tipo_caja')
    list_filter = ('estado',)

admin.site.register(Vehiculo, vehiculoAdmin)
admin.site.register(Detalle, detalleAdmin)
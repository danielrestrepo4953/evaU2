from django.contrib import admin

from django.contrib import admin
from repuestosApp.models import repuestos, descripcion


class repuestosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'stock', 'detalle', 'imagen', 'creado')
    search_fields = ('codigo', 'nombre', 'precio', 'stock', 'detalle')
    list_filter = ('creado',)
    ordering = ('nombre',)

class descripcionAdmin(admin.ModelAdmin):
    list_display = ('repuesto', 'descripcion')
    search_fields = ('repuesto__nombre', 'descripcion')
    list_filter = ('repuesto',)
    ordering = ('repuesto',)

admin.site.register(repuestos, repuestosAdmin)
admin.site.register(descripcion, descripcionAdmin)

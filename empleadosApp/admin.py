from django.contrib import admin
from empleadosApp.models import Empleado, DetalleEmpleado
# Register your models here.
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "apellido", "cargo")
    search_fields = ("rut", "nombre", "apellido", "cargo")
    list_filter = ("cargo",)
    ordering = ("apellido", "nombre")
    
class DetalleEmpleadoAdmin(admin.ModelAdmin):
    list_display = ("empleado", "direccion", "fecha_contratacion", "telefono", "correo", "creado")
    search_fields = ("empleado__nombre", "empleado__apellido", "direccion", "telefono", "correo")
    list_filter = ("fecha_contratacion", "creado")
    ordering = ("empleado__apellido", "empleado__nombre")
    
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(DetalleEmpleado, DetalleEmpleadoAdmin)

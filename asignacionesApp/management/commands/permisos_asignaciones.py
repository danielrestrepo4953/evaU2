from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

# Qué puede hacer cada perfil con las asignaciones
PERMISOS_POR_GRUPO = {
    'Administrador': ['view', 'add', 'change', 'delete'],
    'Supervisor': ['view', 'add', 'change'],
    'Empleado': ['view'],
}


class Command(BaseCommand):
    help = 'Asigna a cada grupo los permisos de asignacionesApp.'

    def handle(self, *args, **kwargs):

        for nombre_grupo, acciones in PERMISOS_POR_GRUPO.items():
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)

            for accion in acciones:
                permiso = Permission.objects.get(
                    codename=f'{accion}_asignacion',
                    content_type__app_label='asignacionesApp',
                )
                grupo.permissions.add(permiso)

            self.stdout.write(f'{nombre_grupo}: {", ".join(acciones)}')

        self.stdout.write('Permisos de asignaciones aplicados exitosamente.')

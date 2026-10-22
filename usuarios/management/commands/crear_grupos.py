from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Group.objects.get_or_create(name='Administrador')
        Group.objects.get_or_create(name='Supervisor')
        Group.objects.get_or_create(name='Empleado')

        self.stdout.write('Grupos creados exitosamente.')

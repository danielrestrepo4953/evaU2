1. Crear entorno virtual
2. Ejecutar entorno virtual, actualizar el pip (python -m pip install --upgrade pip)
3. Instalar dependencias (pip install -r requirements.txt)
4. Crear archivo .env con las credenciales de base de datos.
5. Agregar IP de la instancia EC2 en settings.py, junto a localhost y 127.0.0.1 para permitir acceso de BD.
6. Agregar la ruta de archivos estaticos en settings.py
7. Clonar archivos estaticos a la ruta del proyecto
8. Asegurarse de que gunicorn y nginx estén corriendo y activados para iniciarse automáticamente al encender el servidor.
9. Cambiar el puerto apache a 8080 para evitar conflictos de puertos con nginx. (asegurarse primero de que el puerto 8080 esté abierto en los grupos de seguridad de la instancia EC2)

SETUP DE ROLES Y PERMISOS:

1. Utilizar python manage.py crear_grupos para crear automáticamente los grupos del proyecto (Administrador, supervisor, empleado), asegurarse de que todas las migraciones estén hechas (python manage.py makemigrations ---> python manage.py migrate)
2. Crear un usuario inicial desde la consola y asignarlo al grupo Administrador.
3. Utilizar el superusuario del proyecto para ingresar a Django Admin y asignar todos los permisos al grupo administrador, designar permisos a los grupos supervisor y empleado también. 
4. Con el usuario administrador, ingresar al proyecto con las credenciales y crear los otros usuarios en el mantenedor de usuarios.


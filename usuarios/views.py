from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth import get_user_model
from usuarios.forms import UsuarioCreationForm, UsuarioUpdateForm
from django.contrib import messages
from django import forms
# Create your views here.
@login_required
@permission_required('auth.view_user', raise_exception=True)
def principal_usuarios(request):
    User = get_user_model()
    usuarios = User.objects.all().order_by('username')
    return render(request, 'usuarios/inicio.html', {'usuarios': usuarios})

@login_required
@permission_required('auth.add_user', raise_exception=True)
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.groups.set(form.cleaned_data['grupo'])
            messages.success(request, "El usuario ha sido creado exitosamente. ")
            return redirect('inicio_usuarios')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required
@permission_required('auth.change_user', raise_exception=True)
def cargar_editar_usuario(request,usuario_id):
    User = get_user_model()
    usuario = User.objects.get(id=usuario_id)
    form = UsuarioCreationForm(instance=usuario)

    if usuario.groups.first() == request.user.groups.first():
        messages.error(request, "No puedes modificar tu propio usuario o usuarios de tu mismo grupo.")
        return redirect('inicio_usuarios')
    return render(request, 'usuarios/crear_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, usuario_id):
    User = get_user_model()
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == 'POST':
       form = UsuarioUpdateForm(request.POST, instance=usuario) 

       if form.is_valid():
           usu = form.save()
           usu.groups.set([form.cleaned_data["grupo"]])

           messages.success(request,"El usuario fue modificado correctamente")
           return redirect('inicio_usuarios')

       return render(request, 'usuarios/crear_usuario.html', {'form':form, 'usuario':usuario})


@login_required
@permission_required('auth.delete_user', raise_exception=True)

def eliminar_usuario(request, usuario_id):
    User = get_user_model()
    usuario = get_object_or_404(User, id=usuario_id)

    if usuario.groups.first() == request.user.groups.first():
            messages.error(request, "No puedes eliminar tu propio usuario o usuarios de tu mismo grupo.")
            return redirect('inicio_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Se ha eliminado al usuario exitosamente')
        return redirect('inicio_usuarios')

    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})
    
        
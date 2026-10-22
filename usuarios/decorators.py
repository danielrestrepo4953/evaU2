from django.shortcuts import redirect

def role_required(role_name):

    #funcion decoradora que toma la vista como argumento
    def decorator(view_func):
        #funcion envolvente que toma la solicitud y los argumentos de la vista
        def wrapper(request, *args, **kwargs):
            #verificamos que el usuario esté autenticado
            if request.user.groups.filter(name=role_name).exists():
                #si el usuario tiene el rol requerido, se llama a la vista original
                return view_func(request, *args, **kwargs)

            #redirigimos al login si el usuario no tiene el rol requerido
            return redirect('login')


        #devolvemos la función envolvente como resultado del decorador (O sea, su resultado)
        return wrapper

    #devolvemos la función decoradora como resultado de role_required.
    return decorator
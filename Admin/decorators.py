from django.shortcuts import redirect

def administrador_login_required(function):
    def wrapper(request, *args, **kwargs):
        codadministrador = request.session.get('codadministrador')
        if codadministrador is None:
            request.session['error'] = 'Debes iniciar sesión'
            return redirect('LoginAdmin')  # Redirige al login si no está autenticado
        return function(request, *args, **kwargs)
    return wrapper
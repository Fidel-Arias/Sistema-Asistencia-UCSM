from django.shortcuts import redirect

def colaborador_login_required(function):
    def wrapper(request, *args, **kwargs):
        codcolaborador = request.session.get('codcolaborador')
        if codcolaborador is None:
            request.session['error'] = 'Debes iniciar sesión'
            return redirect('LoginColaborador')  # Redirige al login si no está autenticado
        return function(request, *args, **kwargs)
    return wrapper
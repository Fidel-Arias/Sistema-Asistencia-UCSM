from django.shortcuts import redirect

def participante_login_required(function):
    def wrapper(request, *args, **kwargs):
        codparticipante = request.session.get('codparticipante')
        if codparticipante is None:
            request.session['error'] = 'Debes iniciar sesión'
            return redirect('Login')  # Redirige al login si no está autenticado
        return function(request, *args, **kwargs)
    return wrapper
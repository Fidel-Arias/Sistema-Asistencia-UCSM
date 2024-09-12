from Admin.models import AdminToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.signing import BadSignature, SignatureExpired
from django.core import signing
from rest_framework import status
from Admin.serializers import AdminSerializer
from Admin.models import MaeAdministrador
from Congreso.models import MaeCongreso
from tipoUsuario.models import MaeTipousuario
from Congreso.nuevo_congreso import creando_nuevo_congreso
from adminMaestros.views import administrador_congreso
from django.contrib.auth.hashers import make_password

import json

@api_view(['GET'])
def activar_admin(request): #Encriptar las contraseñas
    token = request.GET.get('token')
    data = validar_token(token, max_age=3600) #Probando la caducidad del link

    if data == status.HTTP_400_BAD_REQUEST:
        return HttpResponse("URL no válida", status=status.HTTP_400_BAD_REQUEST)

    is_valid = creando_nuevo_congreso(data)

    if is_valid == 'failed':
        return HttpResponse("Error al crear el congreso", status=status.HTTP_400_BAD_REQUEST)
    elif is_valid == 'exists':
        return HttpResponse("El congreso ya existe", status=status.HTTP_400_BAD_REQUEST)
    
    data['idtipo'] = MaeTipousuario.objects.get(dstipo="ADMINISTRADOR").pk
    data['idcongreso'] = MaeCongreso.objects.get(nombre=data['nombreCongreso']).pk

    #Verificar si el admin ya existe
    if not MaeAdministrador.objects.filter(correo=data['correo']).exists():

        #Encriptando la contraseña
        data['contrasenia'] = make_password(data['contrasenia'],hasher='pbkdf2_sha256')

        serializer = AdminSerializer(data=data)

        try:
            if serializer.is_valid():
                admin = serializer.save()
                token = AdminToken.objects.create(admin=admin)

                administrador_Congreso = administrador_congreso(data)
                if administrador_Congreso == False:
                    html_error = """
                        <html>
                            <body>
                                <h1>Error en el servidor</h1>
                                <p>Error al crear el administrador en el congreso o</p><br>
                                <p>El administrador ya existe en el congreso</p>
                            </body>
                        </html>
                    """
                    return HttpResponse(html_error, status=status.HTTP_400_BAD_REQUEST)

                html = """<html>
                            <body>
                                <h1>Administrador creado con exito</h1>
                                <p>Puede cerrar esta pestaña</p>
                            </body>
                        </html>"""

                return HttpResponse(html, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("El administrador ya existe", status=status.HTTP_400_BAD_REQUEST)


def validar_token(token, max_age):
    signer = signing.TimestampSigner()
    try:
        data = signer.unsign_object(token, max_age=max_age)
        data = json.loads(data)
        return data
    except (BadSignature, SignatureExpired, Exception ):
        return status.HTTP_400_BAD_REQUEST
    
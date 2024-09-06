from config import settings
from django.core.mail import EmailMultiAlternatives, get_connection, BadHeaderError
from premailer import transform

# Create your views here.
def email_service(request, formulario_data, template, plain_message, subject, to_email, image_path=None):

    # Configurando dinámicamente el email_host_user y el email_host_password
    settings.EMAIL_HOST_USER = formulario_data['correo']
    settings.EMAIL_HOST_PASSWORD = formulario_data['contrasenia']

    # Crear una nueva conexión SMTP con las credenciales dinámicas
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
    )
    
    template = transform(template)

    try:
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
            connection=connection,  # Utilizar la conexión con las nuevas credenciales
        )

        if template:
            email_message.attach_alternative(template, 'text/html')
        
        if image_path:
            with open(image_path, 'rb') as img:
                email_message.attach('Código QR', img.read(), 'image/png')

        #Envio de correo
        email_message.send()

        # Cerrar la conexión SMTP
        connection.close()
        
        return 'success'
    except BadHeaderError:
        print("Encabezado inválido.")
        return 'failed'
    except Exception as e:
        print("Error SMTP: ", e)
        return 'failed'
    
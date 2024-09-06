from django.core import signing
import json

def generar_token(data):
    signer = signing.TimestampSigner()
    data_serializado = json.dumps(data)
    token = signer.sign_object(data_serializado)
    return token
from django.db import models
from tipoUsuario.models import MaeTipousuario
import uuid

# Create your models here.
class MaeAdministrador(models.Model):
    idadministrador = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    correo = models.CharField(max_length=50)
    contrasenia = models.CharField()
    idtipo = models.ForeignKey(MaeTipousuario, models.DO_NOTHING, db_column='idtipo')
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_administrador'
    
    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class AdminToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True, null=False, default=uuid.uuid4)
    admin = models.ForeignKey(MaeAdministrador, null=False, on_delete=models.CASCADE, related_name='auth_token')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('admin','key')

    def __str__(self):
        return self.key
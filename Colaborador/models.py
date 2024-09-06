from django.db import models
from tipoUsuario.models import MaeTipousuario

# Create your models here.
class MaeColaborador(models.Model):
    idcolaborador = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    correo = models.CharField(max_length=40)
    contrasenia = models.CharField()
    idtipo = models.ForeignKey(MaeTipousuario, models.DO_NOTHING, db_column='idtipo')
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_colaborador'

    def __str__(self) -> str:
        return self.nombres + ' ' + self.apellidos
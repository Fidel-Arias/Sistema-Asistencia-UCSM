from django.db import models

# Create your models here.
class MaeTipousuario(models.Model):
    idtipo = models.AutoField(primary_key=True)
    dstipo = models.CharField(max_length=30)
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_tipousuario'

    def __str__(self):
        return self.dstipo
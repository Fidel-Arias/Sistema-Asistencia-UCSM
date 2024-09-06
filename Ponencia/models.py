from django.db import models
from Congreso.models import MaeCongreso
from Ponente.models import MaePonente

# Create your models here.
class MaePonencia(models.Model):
    idponencia = models.AutoField(primary_key=True)
    idponente = models.ForeignKey(MaePonente, models.DO_NOTHING, db_column='idponente')
    nombre = models.CharField(max_length=255)
    idcongreso = models.ForeignKey(MaeCongreso, models.DO_NOTHING, db_column='idcongreso')
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_ponencia'

    def __str__(self):
        return f'{self.nombre}'
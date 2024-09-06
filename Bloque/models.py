from django.db import models
from Ponencia.models import MaePonencia
from Dia.models import MaeDia
from Ubicacion.models import MaeUbicacion

# Create your models here.
class MaeBloque(models.Model):
    idbloque = models.AutoField(primary_key=True)
    idponencia = models.ForeignKey(MaePonencia, models.DO_NOTHING, db_column='idponencia')
    iddia = models.ForeignKey(MaeDia, models.DO_NOTHING, db_column='iddia')
    horainicio = models.TimeField()
    horafin = models.TimeField()
    idubicacion = models.ForeignKey(MaeUbicacion, models.DO_NOTHING, db_column='idubicacion')
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_bloque'
    
    def __str__(self):
        return f'{(self.horainicio.strftime("%H:%M %p")).lower()} - {(self.horafin.strftime("%H:%M %p")).lower()} : {self.idponencia}'
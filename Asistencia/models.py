from django.db import models
from ParticipanteCongreso.models import ParticipanteCongreso
from BloqueColaborador.models import BloqueColaborador
from Congreso.models import MaeCongreso

# Create your models here.
class TrsAsistencia(models.Model):
    idasistencia = models.AutoField(primary_key=True)
    idpc = models.ForeignKey(ParticipanteCongreso, models.DO_NOTHING, db_column='idpc')
    idbc = models.ForeignKey(BloqueColaborador, models.DO_NOTHING, db_column='idbc')
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    idcongreso = models.ForeignKey(MaeCongreso, models.DO_NOTHING, db_column='idcongreso')

    class Meta:
        managed = False
        db_table = 'trs_asistencia'
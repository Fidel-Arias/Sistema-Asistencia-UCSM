from django.db import models
from Participantes.models import MaeParticipantes
from Congreso.models import MaeCongreso

# Create your models here.
class ParticipanteCongreso(models.Model):
    idpc = models.AutoField(primary_key=True)
    codparticipante = models.ForeignKey(MaeParticipantes, models.DO_NOTHING, db_column='codparticipante')
    idcongreso = models.ForeignKey(MaeCongreso, models.DO_NOTHING, db_column='idcongreso')

    class Meta:
        managed = False
        db_table = 'participante_congreso'
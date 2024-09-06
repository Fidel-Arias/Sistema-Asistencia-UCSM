from django.db import models
from Colaborador.models import MaeColaborador
from Bloque.models import MaeBloque
from Congreso.models import MaeCongreso

# Create your models here.
class BloqueColaborador(models.Model):
    idbc = models.AutoField(primary_key=True)
    idcolaborador = models.ForeignKey(MaeColaborador, models.DO_NOTHING, db_column='idcolaborador')
    idbloque = models.ForeignKey(MaeBloque, models.DO_NOTHING, db_column='idbloque')
    idcongreso = models.ForeignKey(MaeCongreso, models.DO_NOTHING, db_column='idcongreso')
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'bloque_colaborador'
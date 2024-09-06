from django.db import models
from tipoDocumento.models import MaeTipodocumento
from tipoParticipante.models import MaeTipoParticipante

# Create your models here.
class MaeParticipantes(models.Model):
    codparticipante = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=50)
    ap_materno = models.CharField(max_length=40)
    ap_paterno = models.CharField(max_length=40)
    correo = models.CharField(max_length=40)
    idtipodoc = models.ForeignKey(MaeTipodocumento, models.DO_NOTHING, db_column='idtipodoc')
    idtipo = models.ForeignKey(MaeTipoParticipante, models.DO_NOTHING, db_column='idtipo')
    qr_code = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mae_participantes'

    def __str__(self) -> str:
        return self.nombre + self.ap_paterno + self.ap_materno
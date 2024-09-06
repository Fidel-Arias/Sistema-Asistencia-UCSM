from Admin.models import MaeAdministrador
from BloqueColaborador.models import BloqueColaborador
from Colaborador.models import MaeColaborador
from Bloque.models import MaeBloque
from Ponente.models import MaePonente
from Ponencia.models import MaePonencia
from Congreso.models import MaeCongreso
from django.db import models

class AdministradorBloquecolaborador(models.Model):
    idabc = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idbc = models.ForeignKey(BloqueColaborador, models.DO_NOTHING, db_column='idbc')

    class Meta:
        managed = False
        db_table = 'administrador_bloquecolaborador'


class AdministradorBloques(models.Model):
    idab = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idbloque = models.ForeignKey(MaeBloque, models.DO_NOTHING, db_column='idbloque')

    class Meta:
        managed = False
        db_table = 'administrador_bloques'


class AdministradorColaborador(models.Model):
    idac = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idcolaborador = models.ForeignKey(MaeColaborador, models.DO_NOTHING, db_column='idcolaborador')

    class Meta:
        managed = False
        db_table = 'administrador_colaborador'


class AdministradorCongreso(models.Model):
    idac = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idcongreso = models.ForeignKey(MaeCongreso, models.DO_NOTHING, db_column='idcongreso')

    class Meta:
        managed = False
        db_table = 'administrador_congreso'


class AdministradorPonencias(models.Model):
    idap = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idponencia = models.ForeignKey(MaePonencia, models.DO_NOTHING, db_column='idponencia')

    class Meta:
        managed = False
        db_table = 'administrador_ponencias'


class AdministradorPonentes(models.Model):
    idapt = models.AutoField(primary_key=True)
    idadministrador = models.ForeignKey(MaeAdministrador, models.DO_NOTHING, db_column='idadministrador')
    idponente = models.ForeignKey(MaePonente, models.DO_NOTHING, db_column='idponente')

    class Meta:
        managed = False
        db_table = 'administrador_ponentes'


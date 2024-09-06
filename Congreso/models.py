from django.db import models

# Create your models here.
class MaeCongreso(models.Model):
    idcongreso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    asistenciatotal = models.IntegerField()
    estado = models.CharField(max_length=11, default='ACTIVO')

    class Meta:
        managed = False
        db_table = 'mae_congreso'

    def __str__(self) -> str:
        return self.nombre
from django.db import models

# Create your models here.
class MaeUbicacion(models.Model):
    idubicacion = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=60)
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_ubicacion'
    
    def __str__(self) -> str:
        return self.ubicacion
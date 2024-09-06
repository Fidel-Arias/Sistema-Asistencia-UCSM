from django.db import models

# Create your models here.
class MaePonente(models.Model):
    idponente = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    estado = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'mae_ponente'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
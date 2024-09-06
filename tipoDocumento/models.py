from django.db import models

# Create your models here.
class MaeTipodocumento(models.Model):
    idtipodoc = models.AutoField(primary_key=True)
    dsdoc = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mae_tipodocumento'
    
    def __str__(self) -> str:
        return self.dsdoc
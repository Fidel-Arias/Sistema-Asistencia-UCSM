# Generated by Django 5.1.1 on 2024-09-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MaeTipoParticipante",
            fields=[
                ("idtipo", models.AutoField(primary_key=True, serialize=False)),
                ("dstipo", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "mae_tipo_participante",
                "managed": False,
            },
        ),
    ]

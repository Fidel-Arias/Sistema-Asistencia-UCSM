# Generated by Django 5.1.1 on 2024-09-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MaeBloque",
            fields=[
                ("idbloque", models.AutoField(primary_key=True, serialize=False)),
                ("horainicio", models.TimeField()),
                ("horafin", models.TimeField()),
                ("estado", models.CharField(max_length=11)),
            ],
            options={
                "db_table": "mae_bloque",
                "managed": False,
            },
        ),
    ]

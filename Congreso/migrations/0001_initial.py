# Generated by Django 5.1.1 on 2024-09-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MaeCongreso",
            fields=[
                ("idcongreso", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(blank=True, max_length=200, null=True)),
                ("fechainicio", models.DateField()),
                ("fechafin", models.DateField()),
                ("asistenciatotal", models.IntegerField()),
                ("estado", models.CharField(max_length=11)),
            ],
            options={
                "db_table": "mae_congreso",
                "managed": False,
            },
        ),
    ]

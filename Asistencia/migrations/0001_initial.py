# Generated by Django 5.1.1 on 2024-09-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TrsAsistencia",
            fields=[
                ("idasistencia", models.AutoField(primary_key=True, serialize=False)),
                ("fecha", models.DateField()),
                ("hora", models.TimeField()),
                ("estado", models.CharField(max_length=11)),
            ],
            options={
                "db_table": "trs_asistencia",
                "managed": False,
            },
        ),
    ]

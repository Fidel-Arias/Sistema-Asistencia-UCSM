# Generated by Django 5.1.1 on 2024-09-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ParticipanteCongreso",
            fields=[
                ("idpc", models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "participante_congreso",
                "managed": False,
            },
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-15 23:01

from django.db import migrations, models
import suapfake.models


class Migration(migrations.Migration):
    dependencies = [
        ("suapfake", "0003_alter_diario_pacote_enviado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diario",
            name="pacote_enviado",
            field=models.JSONField(
                default=suapfake.models.get_default_pacote,
                verbose_name="pacote a enviar/enviado",
            ),
        ),
    ]

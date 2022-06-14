# Generated by Django 4.0.5 on 2022-06-14 22:33

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_alter_turma_options_alter_ambiente_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambiente',
            name='sigla',
            field=models.CharField(max_length=255, unique=True, verbose_name='sigla do ambiente'),
        ),
        migrations.AlterField(
            model_name='diario',
            name='codigo',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('(\\d{5}\\.\\d\\.\\d{5}\\...)\\.(.*\\..*)'))], verbose_name='código do diário'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20170413_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='categoria',
            field=models.CharField(choices=[('noche', 'Noche'), ('comer', 'Comer'), ('tapeo', 'Tapas'), ('dulce', 'Dulce'), ('varios', 'Varios')], default='varios', max_length=10),
        ),
    ]

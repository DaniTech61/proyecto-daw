# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 17:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_comentarios_turismo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentarios',
            old_name='título',
            new_name='titulo',
        ),
    ]
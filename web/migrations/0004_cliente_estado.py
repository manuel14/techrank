# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20171118_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.CharField(choices=[('NO', 'No contactado'), ('CT', 'contactado'), ('VE', 'venta confirmada')], default='NO', max_length=20),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-06 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lorikeet', '0009_auto_20170306_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
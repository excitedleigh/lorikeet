# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-13 01:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lorikeet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='lorikeet.Cart'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='lorikeet.Order'),
        ),
    ]
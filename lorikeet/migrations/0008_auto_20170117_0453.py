# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-17 04:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lorikeet', '0007_deliveryaddress_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lorikeet.DeliveryAddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lorikeet.Payment'),
        ),
    ]
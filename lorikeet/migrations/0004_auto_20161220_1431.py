# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-20 04:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lorikeet", "0003_auto_20161220_1313"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="delivery_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lorikeet.DeliveryAddress",
            ),
        ),
        migrations.AlterField(
            model_name="deliveryaddress",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="delivery_addresses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

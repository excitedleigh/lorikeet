# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-07 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lorikeet", "0011_lineitem_total_when_charged"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

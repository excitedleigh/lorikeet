# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-05-02 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe', '0003_auto_20170502_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecard',
            name='reusable',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stripecard',
            name='token_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='stripecard',
            name='card_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='stripecard',
            name='customer_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

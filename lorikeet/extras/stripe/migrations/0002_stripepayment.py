# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-18 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lorikeet", "0008_auto_20170117_0453"),
        ("stripe", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StripePayment",
            fields=[
                (
                    "payment_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="lorikeet.Payment",
                    ),
                ),
                ("charge_id", models.CharField(max_length=30)),
            ],
            bases=("lorikeet.payment",),
        ),
    ]

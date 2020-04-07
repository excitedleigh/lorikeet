# Generated by Django 2.2.12 on 2020-04-07 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lorikeet", "0016_adjustment_total_when_charged"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="delivery_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lorikeet.DeliveryAddress",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="payment_method",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lorikeet.PaymentMethod",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="lineitem",
            name="cart",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="items",
                to="lorikeet.Cart",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="delivery_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lorikeet.DeliveryAddress",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lorikeet.Payment",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="method",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="lorikeet.PaymentMethod"
            ),
        ),
    ]
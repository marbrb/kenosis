# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-11 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_auto_20171009_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='is_pay_with_card',
            field=models.BooleanField(default=False, verbose_name='Fue pago con tarjeta de credito'),
        ),
        migrations.AddField(
            model_name='register',
            name='product_name',
            field=models.CharField(default='nombre jeje', max_length=255, verbose_name='nombre del producto'),
            preserve_default=False,
        ),
    ]
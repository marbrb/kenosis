# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_auto_20171020_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='código'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_auto_20171011_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='fecha'),
        ),
    ]

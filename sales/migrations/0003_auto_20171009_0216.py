# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 02:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20171009_0214'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='register',
            name='client',
        ),
        migrations.RemoveField(
            model_name='register',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Register',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-06-22 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redirect',
            name='destination',
        ),
        migrations.AddField(
            model_name='redirect',
            name='reference_id',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0002_auto_20160622_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr/'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-13 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20180913_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedatahistory',
            name='deleted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

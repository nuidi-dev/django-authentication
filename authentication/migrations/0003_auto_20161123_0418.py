# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 04:18
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20161123_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='key',
            field=models.UUIDField(blank=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='account',
            name='keytime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_auto_20161227_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='uinfo',
            name='avatar',
            field=models.ImageField(null=True, upload_to='avatar'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 07:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_auto_20170525_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseballplayer',
            options={'verbose_name': '選手', 'verbose_name_plural': '選手'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': '球団', 'verbose_name_plural': '球団'},
        ),
    ]

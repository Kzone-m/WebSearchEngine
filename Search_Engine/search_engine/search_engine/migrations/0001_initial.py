# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=100, verbose_name='索引')),
            ],
            options={
                'verbose_name': '索引',
                'verbose_name_plural': '索引',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, verbose_name='URL')),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_engine.Index')),
            ],
            options={
                'verbose_name': 'URL',
                'verbose_name_plural': 'URL',
            },
        ),
    ]
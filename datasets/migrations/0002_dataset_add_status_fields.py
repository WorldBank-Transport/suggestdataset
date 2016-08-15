# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-15 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='is_open_issue',
            field=models.BooleanField(default=True, verbose_name='The issue is open'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.CharField(blank=True, choices=[('under review', 'Under review'), ('in progress', 'In progress'), ('published', 'Published on Open Data Portal'), ('not public', 'Not for public')], default='under review', max_length=255, verbose_name='Status'),
        ),
    ]

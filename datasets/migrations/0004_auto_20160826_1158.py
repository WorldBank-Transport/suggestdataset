# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-26 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_add_dataset_suggester_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Dataset name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Dataset name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name_sw',
            field=models.CharField(max_length=128, null=True, verbose_name='Dataset name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='suggester_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='Suggester name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='suggester_organization',
            field=models.CharField(blank=True, max_length=128, verbose_name='Suggester organization'),
        ),
    ]

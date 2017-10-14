# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-14 00:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20170904_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('line_number', models.IntegerField()),
                ('source_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SourceFile')),
            ],
        ),
    ]

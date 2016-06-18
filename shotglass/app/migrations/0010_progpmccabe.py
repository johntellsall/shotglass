# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20160612_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgPmccabe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified_mccabe', models.IntegerField()),
                ('mccabe', models.IntegerField()),
                ('num_statements', models.IntegerField()),
                ('first_line', models.IntegerField()),
                ('num_lines', models.IntegerField()),
                ('definition_line', models.IntegerField()),
            ],
        ),
    ]

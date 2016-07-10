# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160622_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skeleton',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('color', colorfield.fields.ColorField(max_length=10)),
                ('sourceline', models.ForeignKey(blank=True, to='app.SourceLine', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='diagramsymbol',
            name='sourceline',
        ),
        migrations.DeleteModel(
            name='DiagramSymbol',
        ),
    ]

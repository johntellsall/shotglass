# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150705_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourceline',
            name='kind',
            field=models.CharField(max_length=12),
        ),
    ]

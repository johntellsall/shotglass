# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20160612_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourceline',
            name='path',
            field=models.CharField(max_length=200),
        ),
    ]

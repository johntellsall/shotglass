# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_diagramsymbol'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diagramsymbol',
            old_name='pen',
            new_name='color',
        ),
    ]

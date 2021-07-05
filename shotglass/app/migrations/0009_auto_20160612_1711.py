# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_auto_20160529_0220"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diagramsymbol",
            name="sourceline",
            field=models.ForeignKey(blank=True, to="app.SourceLine", null=True),
        ),
    ]

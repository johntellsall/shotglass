# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_sourceline_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourceline",
            name="length",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

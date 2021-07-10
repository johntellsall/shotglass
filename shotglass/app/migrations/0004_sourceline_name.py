# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_auto_20150705_0553"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourceline",
            name="name",
            field=models.CharField(default="na", max_length=200),
            preserve_default=False,
        ),
    ]

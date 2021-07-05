# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_sourceline_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourceline",
            name="tags_json",
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]

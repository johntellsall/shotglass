# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_merge"),
    ]

    operations = [
        migrations.AlterField(
            model_name="progpmccabe",
            name="sourceline",
            field=models.OneToOneField(
                null=True, blank=True, to="app.SourceLine", on_delete=models.CASCADE
            ),
        ),
    ]

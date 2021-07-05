# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_progpmccabe"),
    ]

    operations = [
        migrations.AddField(
            model_name="progpmccabe",
            name="sourceline",
            field=models.ForeignKey(blank=True, to="app.SourceLine", null=True, on_delete=models.CASCADE),
        ),
    ]

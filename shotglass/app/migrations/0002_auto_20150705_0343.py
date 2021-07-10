# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourceline",
            name="project",
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]

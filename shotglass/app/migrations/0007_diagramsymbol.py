# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_sourceline_tags_json"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiagramSymbol",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("position", models.IntegerField()),
                ("x", models.IntegerField()),
                ("y", models.IntegerField()),
                ("pen", colorfield.fields.ColorField(max_length=10)),
                ("sourceline", models.ForeignKey(to="app.SourceLine")),
            ],
        ),
    ]

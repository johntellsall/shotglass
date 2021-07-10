# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_remove_sourceline_tags_json"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgRadon",
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
                ("type", models.CharField(max_length=1)),
                ("complexity", models.IntegerField()),
                (
                    "sourceline",
                    models.OneToOneField(
                        null=True,
                        blank=True,
                        to="app.SourceLine",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SourceLine",
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
                ("project", models.CharField(max_length=200)),
                ("path", models.CharField(max_length=20)),
                ("line_number", models.IntegerField()),
                (
                    "kind",
                    models.CharField(
                        max_length=2,
                        choices=[
                            (b"f", b"function"),
                            (b"v", b"variable"),
                            (b"s", b"struct"),
                            (b"c", b"macro"),
                            (b"m", b"member"),
                        ],
                    ),
                ),
            ],
        ),
    ]

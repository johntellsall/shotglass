# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0016_progradon"),
    ]

    operations = [
        migrations.RenameField(
            model_name="progradon",
            old_name="type",
            new_name="kind",
        ),
    ]

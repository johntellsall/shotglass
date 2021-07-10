# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_auto_20160618_1946"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sourceline",
            name="tags_json",
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-10 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20210710_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='length',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

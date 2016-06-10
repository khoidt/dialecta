# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_auto_20151102_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='year_of_death',
            field=models.IntegerField(null=True),
        ),
    ]

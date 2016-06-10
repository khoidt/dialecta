# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_auto_20151102_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='relations',
        ),
        migrations.RemoveField(
            model_name='personalrelation',
            name='from_person',
        ),
        migrations.RemoveField(
            model_name='personalrelation',
            name='to_person',
        ),
    ]

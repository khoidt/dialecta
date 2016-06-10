# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20150909_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='person',
            name='year_of_birth',
            field=models.IntegerField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0004_auto_20150920_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='transcriptions',
        ),
        migrations.AddField(
            model_name='form',
            name='value',
            field=models.CharField(max_length=30, default=''),
            preserve_default=False,
        ),
    ]

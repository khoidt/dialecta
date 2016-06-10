# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0005_auto_20150920_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='data',
            field=models.FilePathField(),
        ),
    ]

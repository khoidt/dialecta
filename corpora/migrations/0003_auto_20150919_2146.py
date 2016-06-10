# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0002_auto_20150919_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus',
            name='to_files',
            field=models.ManyToManyField(to='corpora.File', verbose_name='files'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0006_auto_20150921_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='data',
            field=models.FileField(upload_to=''),
        ),
    ]

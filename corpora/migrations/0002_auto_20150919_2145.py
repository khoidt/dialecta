# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='corpus',
            name='to_dialects',
        ),
        migrations.AddField(
            model_name='corpus',
            name='to_files',
            field=models.ManyToManyField(verbose_name='files', to='corpora.Dialect'),
        ),
    ]

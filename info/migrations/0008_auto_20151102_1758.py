# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0007_auto_20151102_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='relations',
            field=models.ManyToManyField(null=True, to='info.Person', through='info.PersonalRelation'),
        ),
        migrations.AddField(
            model_name='personalrelation',
            name='from_person',
            field=models.ForeignKey(default='', to='info.Person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalrelation',
            name='to_person',
            field=models.ForeignKey(related_name='related_person', default='', to='info.Person'),
            preserve_default=False,
        ),
    ]

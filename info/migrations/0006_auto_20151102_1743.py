# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20151102_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='relations',
            field=models.ManyToManyField(related_name='related_to', to='info.Person', through='info.PersonalRelation'),
        ),
        migrations.AddField(
            model_name='personalrelation',
            name='from_person',
            field=models.ForeignKey(to='info.Person', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalrelation',
            name='to_person',
            field=models.ForeignKey(related_name='related_person', default='', to='info.Person'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_person_year_of_death'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalrelation',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='relations',
            field=models.ManyToManyField(through='info.PersonalRelation', to='info.Person'),
        ),
    ]

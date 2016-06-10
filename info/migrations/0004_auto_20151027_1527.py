# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20150919_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(max_length=15)),
                ('to_person', models.ForeignKey(to='info.Person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='relations',
            field=models.ManyToManyField(through='info.PersonalRelation', to='info.Person'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('last_name', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=15)),
                ('patronimic_name', models.CharField(max_length=20, blank=True)),
                ('sex', models.CharField(choices=[('m', 'Masculine'), ('f', 'Feminine')], max_length=1, blank=True)),
                ('year_of_birth', models.IntegerField(null=True, max_length=4)),
                ('place_of_birth', models.ForeignKey(to='info.Address')),
            ],
        ),
    ]

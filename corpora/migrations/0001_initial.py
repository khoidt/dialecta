# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Corpora',
            },
        ),
        migrations.CreateModel(
            name='Dialect',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('abbreviation', models.CharField(max_length=5)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('abbreviation', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='dialect',
            name='to_language',
            field=models.ForeignKey(to='corpora.Language'),
        ),
        migrations.AddField(
            model_name='corpus',
            name='to_dialects',
            field=models.ManyToManyField(to='corpora.Dialect'),
        ),
    ]

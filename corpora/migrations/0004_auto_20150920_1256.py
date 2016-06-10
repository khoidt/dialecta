# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpora', '0003_auto_20150919_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('transcriptions', models.TextField()),
                ('annotation', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30)),
                ('POS', models.CharField(max_length=10)),
                ('to_language', models.ForeignKey(to='corpora.Language')),
            ],
            options={
                'verbose_name_plural': 'Lemmata',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('transcription', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TokenToForm',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('to_form', models.ForeignKey(to='corpora.Form')),
                ('to_token', models.ForeignKey(to='corpora.Token')),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='to_forms',
            field=models.ManyToManyField(through='corpora.TokenToForm', to='corpora.Form'),
        ),
        migrations.AddField(
            model_name='form',
            name='to_lemma',
            field=models.ForeignKey(verbose_name='to lemma(ta)', to='corpora.Lemma'),
        ),
    ]

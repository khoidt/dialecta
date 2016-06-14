#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os, sndhdr
from info.models import *
from django.utils import timezone


class OverwriteStorage(FileSystemStorage):

    '''
    Overwrite media files when an old one with the same name exists
    '''
    
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Language(models.Model):
  
  name = models.CharField(max_length=50)
  abbreviation = models.CharField(max_length=5)

  def __str__(self):
    return self.abbreviation

class Dialect(models.Model):
  
  name = models.CharField(max_length=50)
  abbreviation = models.CharField(max_length=5)
  to_language = models.ForeignKey('Language')
  description = models.TextField(blank=True)

  def __str__(self):
    return self.abbreviation

class Lemma(models.Model):

  value = models.CharField(max_length=30)
  POS = models.CharField(max_length=10)
  to_language = models.ForeignKey('Language')
  
  class Meta:
    verbose_name_plural = 'Lemmata'

  def __str__(self):
    return self.value

class Form(models.Model):

  value = models.CharField(max_length=30)
  to_lemma = models.ForeignKey(Lemma, verbose_name='to lemma(ta)')
  annotation = models.CharField(max_length=30)
  
  def __str__(self):
    return self.value

class TokenToForm(models.Model):

  order_id = models.IntegerField()
  to_form = models.ForeignKey('Form')
  to_token = models.ForeignKey('Token')

class Token(models.Model):

  transcription = models.CharField(max_length=50)
  to_forms = models.ManyToManyField('Form', through='TokenToForm')

class Recording(models.Model):
  
  string_id = models.CharField(max_length=30,verbose_name='String ID')
  recording_date = models.DateField(default=timezone.now)
  recording_time = models.TimeField(blank=True, null=True)
  recording_place = models.ForeignKey(Location, blank=True, null=True)
  data = models.FileField(storage=OverwriteStorage())
  audio = models.FileField(storage=OverwriteStorage(), null=True)
  recording_device = models.CharField(max_length=60, blank=True)
  to_dialect = models.ForeignKey('Dialect', blank=True, null=True,
                                      verbose_name='Dialect')
  to_speakers = models.ManyToManyField(Speaker, blank=True,
                                      verbose_name='Speakers')
  to_interviewers = models.ManyToManyField(Interviewer, blank=True,
                                      verbose_name='Interviewers')
  notes = models.TextField(blank=True)
  
  def __str__(self):
    return os.path.basename(self.data.name)[:-4]

  def participants(self):
    from corpora.elan_tools import ElanObject
    if self.data.path:
      try:
        elan_obj = ElanObject(self.data.path)
        return ', '.join(elan_obj.participants_lst)
      except FileNotFoundError:
        pass
    return ''

  def rename_data_file(self, new_name):

    path, old_name = os.path.split(self.data.path)
    new_name = os.path.join(path, '%s.%s' %(new_name, old_name.split('.')[1]))
    os.rename(self.data.path, new_name)
    self.data.name = new_name
    self.save()

  def rename_audio_file(self, new_name):

    path, old_name = os.path.split(self.audio.path)
    new_name = os.path.join(path, '%s.%s' %(new_name, old_name.split('.')[1]))
    os.rename(self.audio.path, new_name)
    self.audio.name = new_name
    self.save()

  def audio_data(self):
    
    if self.audio.path:
      try:
        data = sndhdr.what(self.audio.path)
        data_str = 'filetype: %s, framerate: %s, nchannels: %s, nframes: %s, sampwidth: %s'%(
          data[0], data[1], data[2], data[3], data[4]
          )
        return data_str
      except:
        pass
    return 'None'

  class Meta:
    verbose_name = 'Recording'
    verbose_name_plural = 'Recordings'

class Corpus(models.Model):
  
  to_files = models.ManyToManyField(Recording, verbose_name='Elan data')

  class Meta:
    verbose_name_plural = 'Corpora'

class NormalizationModel(models.Model):

  to_dialect = models.ForeignKey('Dialect')
  to_additional_language = models.ForeignKey('Language', blank=True, null=True)
  examples = models.TextField(blank=True)
  exceptions = models.TextField(blank=True)
  

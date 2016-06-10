from django.db import models

class Language(models.Model):
  
  name = models.CharField(max_length=50)
  abbreviation = models.CharField(max_length=5)

class Dialect(models.Model):
  
  name = models.CharField(max_length=50)
  abbreviation = models.CharField(max_length=5)
  to_language = models.ForeignKey('Language')
  description = models.TextField(blank=True)

class Lemma(models.Model):

  value = models.CharField(max_length=30)
  POS = models.CharField(max_length=10)
  to_language = models.ForeignKey('Language')
  
  class Meta:
    verbose_name_plural = 'Lemmata'

class Form(models.Model):

  value = models.CharField(max_length=30)
  to_lemma = models.ForeignKey(Lemma, verbose_name='to lemma(ta)')
  annotation = models.CharField(max_length=30)

class TokenToForm(models.Model):

  order_id = models.IntegerField()
  to_form = models.ForeignKey('Form')
  to_token = models.ForeignKey('Token')

class Token(models.Model):

  transcription = models.CharField(max_length=50)
  to_forms = models.ManyToManyField('Form', through='TokenToForm')

class File(models.Model):

  data = models.FileField()

class Corpus(models.Model):
  
  to_files = models.ManyToManyField(File, verbose_name='files')

  class Meta:
    verbose_name_plural = 'Corpora'

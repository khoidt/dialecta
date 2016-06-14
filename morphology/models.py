from django.db import models

class GlossingRule(models.Model):

  abbreviation = models.CharField(max_length=10)
  description = models.TextField(blank=True)
  examples = models.TextField(blank=True)
  abbr_overrides = models.CharField(max_length=100, blank=True)
  section = models.CharField(max_length=10, blank=True)

  def __str__(self):
    return self.abbreviation

  def populate(self, abbreviation, description, examples, abbr_overrides, section):

    self.abbreviation = abbreviation
    self.description = description
    self.examples = examples
    self.abbr_overrides = abbr_overrides
    self.section = section

    self.save()

  



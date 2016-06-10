from django.db import models
from geoposition.fields import GeopositionField
from django.core.exceptions import ObjectDoesNotExist

SEX_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
)

class Location(models.Model):
  
  name = models.CharField(max_length=100)
  position = GeopositionField()

  def __str__(self):
    return self.name

class Person(models.Model):

  last_name = models.CharField(max_length=15,)
  first_name = models.CharField(max_length=15,)
  patronimic_name = models.CharField(max_length=20,
                                     blank=True,
                                     )
  sex = models.CharField(max_length=1, choices=SEX_CHOICES,)
  year_of_birth = models.IntegerField(null=True,)
  year_of_death = models.IntegerField(blank=True,)
  
  place_of_birth = models.ForeignKey(Location)
  
  relations = models.ManyToManyField('self',
                                     through='PersonalRelation',
                                     symmetrical=False,
                                     through_fields=('from_person', 'to_person'),
                                     )


  def __str__(self):

    patr = ''
    if self.patronimic_name !='':
      patr = ' '+self.patronimic_name

    return '%s, %s%s' %(self.last_name, self.first_name, patr)


RELATION_CHOICES = (
  ('ch', 'child'),
  ('pr', 'parent'),
  ('sp', 'spouse'),
  ('sb', 'sibling'),
  ('gc', 'grandchild'),
  ('gp', 'grandparent'),
  ('fr', 'friend'),
  ('ng', 'neighbor'),
  ('lv', 'lover'),
  )

ASYMMETRIC_RELATIONS_DICTIONARY = {
  'ch' : 'pr',
  'pr' : 'ch',
  'gc' : 'gp',
  'gp' : 'gc',
  }

class PersonalRelation(models.Model):

  # Model of defining relations between persons
  
  # Include overrides of model save and delete functions
  # that additionaly create, edit and delete a
  # reverse relation that mirrors the one being modified.

  # Relation types are included in RELATION_CHOICES
  # Pairs of asymmetrc relation types are additionaly listed in the ASYMMETRIC_RELATIONS_DICTIONARY

  from_person = models.ForeignKey('Person')
  to_person = models.ForeignKey('Person',
                                related_name='related_person',
                                )
  relation_type = models.CharField(max_length=15, choices=RELATION_CHOICES)
  notes = models.TextField(blank=True,)

  def save(self, *args, **kwargs):

    older_rev_rel_obj = self.get_reversed_relation_obj()
    super(PersonalRelation, self).save(*args, **kwargs)
    if self.get_reversed_relation_obj() == None:
      if older_rev_rel_obj != None:
        older_rev_rel_obj.delete()
      self.create_reversed_relation()
    else:
      self.update_reversed_relation()
    
  def delete(self, *args, **kwargs):

    rev_rel_obj = self.get_reversed_relation_obj()
    super(PersonalRelation, self).delete(*args, **kwargs)
    if rev_rel_obj != None:
      rev_rel_obj.delete()

  def update_reversed_relation(self):
    
    rev_rel_obj = self.get_reversed_relation_obj()
    if rev_rel_obj.relation_type != self.get_reversed_relation_type() or rev_rel_obj.notes != self.notes:
      rev_rel_obj.relation_type = self.get_reversed_relation_type()
      rev_rel_obj.notes = self.notes
      rev_rel_obj.save()

  def get_reversed_relation_obj(self):

    try:
      rev_rel_obj = PersonalRelation.objects.get(
        from_person = self.to_person,
        to_person = self.from_person,
        )
      return rev_rel_obj
    except ObjectDoesNotExist:
      return None

  def create_reversed_relation(self):

      rev_rel_obj = PersonalRelation(
        from_person = self.to_person,
        to_person = self.from_person,
        relation_type = self.get_reversed_relation_type(),
        notes = self.notes,
      )
      rev_rel_obj.save()
    
  def get_reversed_relation_type(self):

    if self.relation_type in list(ASYMMETRIC_RELATIONS_DICTIONARY.keys()):
      return ASYMMETRIC_RELATIONS_DICTIONARY[self.relation_type]
    return self.relation_type
    

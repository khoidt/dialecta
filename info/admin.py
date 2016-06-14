from django.contrib import admin
from django.db.models import Q
from info.models import *
from reversion.admin import VersionAdmin

class PersonalRelationInline(admin.TabularInline):

  model = PersonalRelation
  extra = 0
  fk_name = 'from_speaker'
  
  def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

    # Overriding to_speaker field choices to avoid recursive relations
    
    field = super(PersonalRelationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)   
    speaker_id = request.path_info.split('/')[-3]
    try:
      speaker_id = int(speaker_id)
      if db_field.name == 'to_speaker' and speaker_id!='add':
        field.queryset = field.queryset.exclude(pk = speaker_id)
    except ValueError:
      pass
    return field

class LocationRelationInline(admin.TabularInline):

    model = LocationRelation
    extra = 1
    verbose_name = 'location'

class LanguageRelationInline(admin.TabularInline):

    model = LanguageRelation
    extra = 1
    verbose_name = 'Language'

@admin.register(Speaker)
class SpeakerAdmin(VersionAdmin):

  list_display = ('last_name', 'first_name','patronimic_name', 'sex', 'year_of_birth', 'education')

  inlines = (PersonalRelationInline,LocationRelationInline,LanguageRelationInline)
  fieldsets = (
    ('Photo', {'fields':(('photo_preview', 'photo')),}),
    ('I. Name', {'fields':(('last_name','first_name'),'patronimic_name', 'other_names'),}),
    ('II. Sex', {'fields':('sex',),}),
    ('III. Years of life', {'fields':(('year_of_birth','year_of_death')),'classes': ('grp-collapse grp-open',)}),
    ('IV. Education', {'fields':('education',),}),
    ('Va. Geography of Life', {'classes': ('placeholder locationrelation_set-group',), 'fields':(),}),
    ('Vb. Mobility', {'fields':('mobility',),}),
    ('VI. Linguistic Biography', {'classes': ('placeholder languagerelation_set-group',), 'fields':(),}),
    ('VII. Relations with other speakers', {'classes': ('placeholder personalrelation_set-group',), 'fields':(),}),
    ('VIII. Profession', {'fields':('profession',),}),
    ('IX. Other', {'fields':('details',),}),
    )
  readonly_fields = ['photo_preview']

@admin.register(Location)
class LocationAdmin(VersionAdmin):
  pass

@admin.register(RelationType)
class RelationTypeAdmin(VersionAdmin):
  pass

@admin.register(EducationType)
class EducationTypeAdmin(VersionAdmin):
  pass

@admin.register(Interviewer)
class EducationInterviewerAdmin(VersionAdmin):
  pass



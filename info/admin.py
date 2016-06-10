from django.contrib import admin
from info.models import *


class PersonalRelationInline(admin.TabularInline):

  model = PersonalRelation
  extra = 0
  fk_name = 'from_person'

  def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

    # Overriding to_person field choices to avoid recursive relations
    
    field = super(PersonalRelationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)   
    person_id = request.path_info.split('/')[-2]
    if db_field.name == 'to_person':
      field.queryset = field.queryset.exclude(pk = person_id)
    return field

class PersonAdmin(admin.ModelAdmin):

  inlines = (PersonalRelationInline,)

admin.site.register(Person, PersonAdmin)
admin.site.register(PersonalRelation)
admin.site.register(Location)

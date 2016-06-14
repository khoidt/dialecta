from django.contrib import admin
from django import forms

from django.db import transaction
from django.conf.urls import include, url
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from corpora.models import *
from info.models import *
from corpora.elan_tools import standartizator, elan_to_html

import json
from django_ajax.decorators import ajax
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


##class RenameCheckboxAdminForm(forms.ModelForm):
##    # custom field not backed by database
##    rename_files_accordingly = forms.BooleanField(initial=False,required=False)
##
##    # REPLACE WITH BUTTON
##    # CONFIRMATION DIALOG
##    # WRITE TO ELAN
##    # CHECK IF SUCH A FILENAME EXISTS
##
##    class Meta:
##        model = Recording
##        fields = "__all__"


class RecordingAdmin(admin.ModelAdmin):

  editor_template = 'editor.html'
  trainer_template = 'trainer.html'
  fields = (('recording_date', 'recording_time', 'recording_place'),
            ('data', 'audio'),
            'recording_device',
            'audio_data', 'participants', 'to_speakers', 'to_interviewers', 'to_dialect',
            ('string_id'),
##          ('string_id', 'rename_files_accordingly'),
            'notes',
            )
  readonly_fields = ('audio_data','participants',)

##  form = RenameCheckboxAdminForm
  save_as=True

  class Media:
    js = ("js/ustie_id.js",)

  def get_urls(self):

    self.processing_request = False
        
    urls = super(RecordingAdmin, self).get_urls()
    my_urls = [url(r'\d+/edit/$', self.admin_site.admin_view(self.edit)),
               url(r'\d+/train/$', self.admin_site.admin_view(self.train)),
               url(r'^ajax/$', self.ajax_dispatcher, name='ajax'),
               ]
    return my_urls + urls

  @transaction.atomic
  def get_valid_string_id(self, request):
    
    date_str = request.POST['request_data[date]']
    person_str = request.POST['request_data[person]']
    #obj = File.objects.get(id = request.path.split('/')[-3])
    #print(File.objects.all().filter(string_id__contains=date_str), obj)
    print(request.path)

  @transaction.atomic
  def edit(self, request):

    self.file_obj = get_object_or_404(File, id=request.path.split('/')[-3])
    self.elan_converter = elan_to_html(self.file_obj)
    
    self.standartizator = standartizator(self.file_obj.to_dialect)
    self.standartizator.start_standartizator()

    annot_menu_select, annot_menu_checkboxes = self.elan_converter.build_annotation_menu()
    
    context = {'ctext': self.elan_converter.html,
               'audio_path': self.file_obj.audio.name,
               'media': self.media['js'],
               'annot_menu_select' : annot_menu_select,
               'annot_menu_checkboxes' : annot_menu_checkboxes,
               }
    return render_to_response(self.editor_template, context_instance=RequestContext(request, context))

  @transaction.atomic
  def train(self, request):

    self.file_obj = get_object_or_404(File, id=request.path.split('/')[-3])
    self.elan_converter = elan_to_html(self.file_obj, 'orth_trainig')
    
    self.standartizator = standartizator(self.file_obj.to_dialect)
    self.standartizator.start_standartizator()
    
    context = {'ctext': self.elan_converter.html,
               'audio_path': self.file_obj.audio.name,
               'media': self.media['js'],
               'examples_dict': json.dumps(self.standartizator.examples_dict),
               'exceptions_lst': json.dumps(self.standartizator.exceptions_lst),
               }
    return render_to_response(self.trainer_template, context_instance=RequestContext(request, context))

  @csrf_exempt
  def ajax_dispatcher(self, request):
      print(request.POST)
      response = {}
      if request.POST == {} or self.processing_request == True:
        return HttpResponse(json.dumps(response))
      self.processing_request = True
      if request.POST['request_type'] == 'save_model_req':
        self.standartizator.update_model(json.loads(request.POST['request_data[trd]']),
                                         json.loads(request.POST['request_data[exr]']),
                                         )
      elif request.POST['request_type'] == 'training_data_load_req':
        response['training_dict'] = self.standartizator.examples_dict
        #response['exceptions_arr'] = self.standartizator.exceptions_lst
      elif request.POST['request_type'] == 'trt_annot_req':
        response['result'] = self.standartizator.generate_dict_for_translit_token(request.POST['request_data[trt]'])
      elif request.POST['request_type'] == 'annot_suggest_req':
        response['result'] = self.standartizator.get_annotation_options_list(request.POST['request_data[nrm]'])
      elif request.POST['request_type'] == 'save_elan_req':
        self.elan_converter.save_html_to_elan(request.POST['request_data[html]'])
      elif request.POST['request_type'] == 'string_id_update':
        response['result'] = self.get_valid_string_id(request)
      self.processing_request = False
      return HttpResponse(json.dumps(response))


admin.site.register(Language)
admin.site.register(Dialect)
admin.site.register(Lemma)
admin.site.register(Form)
admin.site.register(TokenToForm)
admin.site.register(Token)
admin.site.register(Recording, RecordingAdmin)
admin.site.register(Corpus)
admin.site.register(NormalizationModel)

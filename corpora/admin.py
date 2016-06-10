from django.contrib import admin

from django.db import transaction
from django.conf.urls import patterns, include, url
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


from corpora.models import *
from corpora.elan_tools import standartizator, elan_to_html

import json
from django_ajax.decorators import ajax
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class FileAdmin(admin.ModelAdmin):

  editor_template = 'editor.html'

  def get_urls(self):

    self.standartizator = standartizator('RuPS')
    self.standartizator.start_standartizator()
    self.processing_request = False
        
    urls = super(FileAdmin, self).get_urls()
    my_urls = patterns('',
        url(r'\d+/edit/$', self.admin_site.admin_view(self.edit)),
        url(r'^ajax/$', self.ajax_dispatcher, name='ajax'),
    )
    return my_urls + urls

  @transaction.atomic
  def edit(self, request):

    file_id = request.path.split('/')[-3]
    file_obj = get_object_or_404(File, id=file_id)
    self.elan_converter = elan_to_html(file_obj)
    
    context = {'ctext': self.elan_converter.html,
               'audio_path': '/media/'+file_obj.data.name[2:-4]+'.mp3',
               'media': self.media['js'],
               }
    return render_to_response(self.editor_template, context_instance=RequestContext(request, context))

  @csrf_exempt
  def ajax_dispatcher(self, request):
      response = {}
      if request.POST == {} or self.processing_request == True:
        return HttpResponse(json.dumps(response))
      if request.POST['request_type'] == 'trt_annot_req':
        self.processing_request = True
        response['result'] = self.standartizator.generate_dict_for_translit_token(request.POST['request_data[trt]'])
      elif request.POST['request_type'] == 'annot_suggest_req':
        self.processing_request = True
        response['result'] = self.standartizator.get_annotation_options_list(request.POST['request_data[nrm]'])
      elif request.POST['request_type'] == 'save_elan_req':
        self.elan_converter.save_html_to_elan(request.POST['request_data[html]'])
      self.processing_request = False
      return HttpResponse(json.dumps(response))

admin.site.register(Language)
admin.site.register(Dialect)
admin.site.register(Lemma)
admin.site.register(Form)
admin.site.register(TokenToForm)
admin.site.register(Token)
admin.site.register(File, FileAdmin)
admin.site.register(Corpus)

from django.conf.urls import url
from queries import views
from queries import ajax

urlpatterns = [
    url(r'^queries/$', views.queries, name='queries'),
    url(r'^queries/download/$', ajax.download, name='queries_download'),
    url(r'^ajax/$', ajax.query_ajax, name='ajax'),
]


# app.urls

from django.conf.urls import url

from . import views, v_source

urlpatterns = [
    url(r'^$', v_source.source_index),
#    url(r'^$', views.index),
    url(r'(?P<project>\w+)/$', views.list_functions, name='list_functions'),
    url(r'(?P<project>\w+)/overview', views.overview),
]

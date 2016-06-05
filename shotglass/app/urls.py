# app.urls

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_projects),
    url(r'(?P<project>.+)/$', views.list_functions, name='list_functions'),
    url(r'(?P<project>.+)/overview', views.overview, name='overview'),
    url(r'(?P<project>.+)/render', views.render, name='render'),
    url(r'(?P<project>.+)/draw', views.draw, name='draw'),
    url(r'(?P<project>.+)/symbol_index', views.symbol_index),
]

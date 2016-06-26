# app.urls

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.list_projects, name='list_projects'),
    url(r'(?P<project>.+)/$', views.list_symbols, name='list_symbols'),
    url(r'(?P<project>.+)/render', views.render, name='render'),
    url(r'(?P<project>.+)/draw', views.draw, name='draw'),
    url(r'(?P<project>.+)/index_symbols', views.index_symbols,
        name='index_symbols'),
]

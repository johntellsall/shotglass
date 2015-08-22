# app.urls

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'(?P<project>\w+)/$', views.list_functions, name='list_functions'),
    url(r'(?P<project>\w+)/overview', views.overview),
]

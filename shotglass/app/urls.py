# app.urls

from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path(r"^$", views.list_projects, name="list_projects"),
    re_path(r"(?P<project>.+)/$", views.list_symbols, name="list_symbols"),
    re_path(r"(?P<project>.+)/render", views.render, name="render"),
    re_path(r"(?P<project>.+)/draw", views.draw, name="draw"),
    re_path(r"(?P<project>.+)/index_symbols", views.index_symbols, name="index_symbols"),  # noqa: E501
]

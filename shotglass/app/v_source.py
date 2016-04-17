from django.http import HttpResponse
from django.shortcuts import render

from app.models import SourceLine


def source_index(request):
    project = 'flask'
    proj_lines = SourceLine.objects.filter(project=project)
    functions = proj_lines.filter(kind='function').order_by('path', 'name')

    return render(request, 'list_functions2.html', {
        'functions': functions,
        'project': project})

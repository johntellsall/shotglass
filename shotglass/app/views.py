from collections import defaultdict, namedtuple
from django.http import HttpResponse
from django.shortcuts import render

from app.models import SourceLine


def index(request):
    projects = SourceLine.projects()
    return render(request, 'index.html', {'projects': projects})


def overview(request, project):
    proj_lines = SourceLine.objects.filter(project=project)
    def calc_overview():
        prev_lineno = 0
        prev_path = None
        for line in proj_lines.order_by('path', 'line_number'):
            if line.path != prev_path:
                prev_lineno = 0
            info = dict(line.__dict__) # copy
            info['length'] = line.line_number - prev_lineno
            info['bar'] = info['name'][0] * info['length']
            yield info

    return render(request, 'overview.html', {
        'overview': calc_overview,
    })


def list_functions(request, project):
    proj_lines = SourceLine.objects.filter(project=project)
    functions = proj_lines.filter(kind='function').order_by('path', 'name')

    return render(request, 'list_functions2.html', {
        'functions': functions,
        'project': project,
        'symbol_count': proj_lines.count()})

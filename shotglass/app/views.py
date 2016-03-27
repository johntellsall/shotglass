# from django.shortcuts import render

from collections import defaultdict, namedtuple
from django.http import HttpResponse
from django.shortcuts import render

from app.models import SourceLine

def index(request):
    if 0:
        projects = SourceLine.objects.distinct('project')
    else:
        projects = ('flask',)
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

# def overview2(request, project):
#     WIDTH = 1000
#     Block = namedtuple('Block', 'width css_class')

#     proj_source = SourceLine.objects.filter(project=project)
#     prev = None
#     for source in proj_source.order_by('path', 'line_number'):
#         if not prev:
#             prev = source
#             continue
#         info = dict(prev.__dict__)
#         info['length'] = source

#     x = 0
#     css_class = 'light'

#         block = Block(line['
#     def calc_overview():
#         prev_lineno = 0
#         prev_path = None
#             if line.path != prev_path:
#                 prev_lineno = 0
#             info = dict(line.__dict__) # copy
#             info['length'] = line.line_number - prev_lineno
#             yield info

#     def calc_rows():
#         x = 0
#         for info in calc_overview():
#             info['x'] = x
#             yield info
#             x += info['length']
#             if x > WIDTH:
#                 x = 0

#     return render(request, 'overview2.html', {
#         'rows': rows,
#     })


def list_functions(request, project):
    proj_lines = SourceLine.objects.filter(project=project)
    functions = proj_lines.filter(kind='function').order_by('path', 'name')

    return render(request, 'list_functions2.html', {
        'functions': functions,
        'project': project})

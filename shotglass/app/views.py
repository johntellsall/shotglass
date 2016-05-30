import StringIO
from collections import defaultdict, namedtuple
from django.http import HttpResponse
from django import shortcuts
from PIL import Image

from app import render as shotglass_render
from app.models import SourceLine

def index(request):
    projects = SourceLine.projects()
    return shortcuts.render(request, 'index.html', {'projects': projects})


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

    return shortcuts.render(request, 'overview.html', {
        'overview': calc_overview,
    })


def list_functions(request, project):
    proj_lines = SourceLine.objects.filter(project=project)
    functions = proj_lines.filter(kind='function').order_by('path', 'name')

    return shortcuts.render(request, 'list_functions2.html', {
        'functions': functions,
        'project': project,
        'symbol_count': proj_lines.count()})


def render(request, project):
    width = shotglass_render.calc_width(project)
    if not width:
        return HttpResponse(content='uhoh')
    arg = request.GET.get('arg')
    shotglass_render.render(project) # XX
    return HttpResponse(content='okay', content_type='text/plain')


def draw(request, project):     # XX
    """
    draw rendered project into an image
    """
    zoom = float(request.GET.get('zoom', 0.))

    grid = shotglass_render.draw(project) # XX
    image = grid.im

    if zoom > 0.:
        new_size = int(image.size[0]*zoom), int(image.size[1]*zoom)
        image = image.resize(new_size)

    output = StringIO.StringIO()
    image.save(output, format='png')
    output.seek(0)
    return HttpResponse(content=output, content_type='image/png')

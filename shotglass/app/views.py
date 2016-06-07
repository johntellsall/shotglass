import StringIO
from django.http import HttpResponse
from django import shortcuts

from app import render as shotglass_render
from app.models import DiagramSymbol, SourceLine


def list_projects(request):
    projects = SourceLine.projects()
    return shortcuts.render(request, 'list_projects.html', {'projects': projects})


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
    shotglass_render.render(project) # XX
    return HttpResponse(content='okay', content_type='text/plain')


def draw(request, project):     # XX
    """
    draw rendered project into an image
    """
    zoom = float(request.GET.get('zoom', 0.))
    style = request.GET.get('style')
    # tagnum = request.GET.get('tagnum')

    draw_func = {'bbox': shotglass_render.draw_bbox
    }.get(style) or shotglass_render.draw

    grid = draw_func(project) # XX
    image = grid.im

    if zoom > 0.:
        new_size = int(image.size[0]*zoom), int(image.size[1]*zoom)
        image = image.resize(new_size)

    output = StringIO.StringIO()
    image.save(output, format='png')
    output.seek(0)
    return HttpResponse(content=output, content_type='image/png')


def index_symbols(request, project): # X
    # pylint: disable=no-member
    symbols = DiagramSymbol.objects.exclude(
        sourceline__name__startswith='_'
    ).exclude(sourceline__kind__in=['variable']
    ).order_by('sourceline__name')
    return shortcuts.render(request, 'index_symbols.html',
                            dict(project=project, symbols=symbols))

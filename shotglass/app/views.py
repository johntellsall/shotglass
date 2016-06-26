import StringIO

from django import shortcuts
from django.core import urlresolvers
from django.http import HttpResponse

from app import render as shotglass_render
from app.models import DiagramSymbol, SourceLine


def list_projects(request):
    projects = SourceLine.projects()
    return shortcuts.render(request, 'list_projects.html', {
        'projects': projects})


def list_symbols(request, project):
    # pylint: disable=no-member
    proj_lines = SourceLine.objects.filter(project=project)
    symbols = proj_lines.order_by('path', 'name')[:100]
    # TODO: render style menu from this var
    draw_styles = sorted(shotglass_render.DRAW_STYLES.iterkeys())
    return shortcuts.render(request, 'list_symbols.html', {
        'draw_styles': draw_styles,
        'symbols': symbols,
        'project': project,
        'symbol_count': proj_lines.count()})


def render(request, project):
    shotglass_render.render(project) # XX
    return shortcuts.redirect('{}?{}'.format(
        urlresolvers.reverse('draw', kwargs={'project': project}),
        request.META['QUERY_STRING']))


def draw(request, project):     # XX
    """
    draw rendered project into an image
    """
    zoom = float(request.GET.get('zoom', 0.))
    style = request.GET.get('style')

    draw_class = shotglass_render.DRAW_STYLES.get(
        style) or shotglass_render.SimpleDraw

    grid = draw_class().draw(project) # XX
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

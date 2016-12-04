"""
label.py -- 
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import itertools

from django.core.management.base import BaseCommand
from palettable import colorbrewer
from PIL import Image

from app.models import SourceLine


BLACK = (0, 0, 0)
CMAP_OBJ = colorbrewer.qualitative.Set3_12
CMAP_COLORS = map(tuple, CMAP_OBJ.colors)

COL_WIDTH, COL_HEIGHT = 100, 2000
COL_GAP = 10


def serpentine_iter(width):
    y = 0
    while True:
        for x in xrange(width):
            yield x, y
        for x in xrange(width):
            yield width - x - 1, y + 1
        y += 2


def render(funcs, color_gen):
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new('RGB', (width, height))
    im_pixel = im.load()
    image_iter = serpentine_iter(width=width)
    for func in funcs:
        print func.name
        color = color_gen()
        for _ in xrange(func.length):
            im_pixel[image_iter.next()] = color
    return im


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+')

    def handle(self, *args, **options):
        color_iter = itertools.cycle(
            CMAP_COLORS + list(reversed(CMAP_COLORS)))
        # color_iter = itertools.cycle(CMAP_COLORS)

        for project in options['projects']:
            p = SourceLine.objects.filter(project=project)
            print project
            print 'all:', p.count()
            funcs = p.exclude(path__startswith='tests/').exclude(
                path__startswith='examples/')
            print 'no tests:', funcs.count()

            funcs = funcs.order_by('name')
            img = render(funcs, color_iter.next)
            img.save('{}.png'.format(project))

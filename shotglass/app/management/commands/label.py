"""
label.py -- 
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import itertools

from django.core.management.base import BaseCommand
from palettable import colorbrewer
from PIL import Image, ImageDraw

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


def render_funcs(funcs, color_gen):
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new('RGB', (width, height))
    im_pixel = im.load()
    im_draw = ImageDraw.Draw(im)
    image_iter = serpentine_iter(width=width)
    first_ch = None
    new_labels = []
    for func in funcs:
        name = func.name
        new_label = False
        if name[0] != first_ch:
            new_label = True
            first_ch = name[0]
            print func.name
        if new_label:
            new_labels.append([func, image_iter.next()])
        color = color_gen()
        for _ in xrange(func.length):
            im_pixel[image_iter.next()] = color
    print new_labels
    for func, label_pos in new_labels:
        x,y = label_pos
        rect = [x-1,y-1, x+2,y+2]
        im_draw.rectangle(rect, fill='black')
    return im


def render_paths(funcs, color_gen):
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new('RGB', (width, height))
    im_pixel = im.load()
    im_draw = ImageDraw.Draw(im)
    image_iter = serpentine_iter(width=width)
    prev_path = None
    color = None
    for func in funcs:
        if func.path != prev_path:
            prev_path = func.path
            color = color_gen()
            x,y = image_iter.next()
            rect = [x-1,y-1, x+2,y+2]
            im_draw.rectangle(rect, fill='black')
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

            if 0:
                funcs = funcs.order_by('name')
                img = render_funcs(funcs, color_iter.next)
            else:
                funcs = funcs.order_by('path')
                img = render_paths(funcs, color_iter.next)

            img.save('{}.png'.format(project))

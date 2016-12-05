"""
label.py -- 
"""
# pylint: disable=W0640

# list files in Git branch
# git ls-tree --name-status --full-tree -r v4.0.0

import itertools
import re
import subprocess

from django.core.management.base import BaseCommand
from palettable import colorbrewer
from PIL import Image, ImageDraw

from app.models import SourceLine


# BLACK = (0, 0, 0)
# CMAP_OBJ = colorbrewer.qualitative.Set3_12
# CMAP_COLORS = map(tuple, CMAP_OBJ.colors)

COL_WIDTH, COL_HEIGHT = 100, 2000
# COL_GAP = 10


def serpentine_iter(width):
    y = 0
    while True:
        for x in xrange(width):
            yield x, y
        for x in xrange(width):
            yield width - x - 1, y + 1
        y += 2

def render_highlight(path):
    output = subprocess.check_output(
        ['source-highlight', '-i', path])
    output = re.compile('^.+<pre><tt>', re.DOTALL).sub('', output)
    return output.split('\n')


def render(path):
    symbol_re = re.compile('<(.+?)>([^<]*)')
    hlines = render_highlight(path)[:20]
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new('RGB', (width, height))
    # im_pixel = im.load()
    im_draw = ImageDraw.Draw(im)
    colors = ['#808080']
    for y,line in enumerate(hlines):
        print '\t*', line
        x = 0
        mgroups = (match.groups() for match in symbol_re.finditer(line))
        for sym, text in mgroups:
            if sym.startswith('font '):
                colors.append(sym.split('#')[1])
            elif sym == '/font':
                colors.pop()
            if not text:
                continue
            print colors[-1], '"{}"'.format(text)
    # return

    # width = COL_WIDTH
    # height = COL_HEIGHT
    # im = Image.new('RGB', (width, height))
    # im_pixel = im.load()
    # im_draw = ImageDraw.Draw(im)
    # image_iter = serpentine_iter(width=width)
    # prev_path = None
    # color = None
    # for func in funcs:
    #     if func.path != prev_path:
    #         prev_path = func.path
    #         color = color_gen()
    #         x,y = image_iter.next()
    #         rect = [x-1,y-1, x+2,y+2]
    #         im_draw.rectangle(rect, fill='black')
    #     for _ in xrange(func.length):
    #         im_pixel[image_iter.next()] = color
    # return im


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+')

    def handle(self, *args, **options):
        # color_iter = itertools.cycle(
        #     CMAP_COLORS + list(reversed(CMAP_COLORS)))

        for path in options['paths']:
            render(path)
        # img.save('{}.png'.format(project))

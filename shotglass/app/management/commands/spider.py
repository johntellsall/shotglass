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
    hlines = render_highlight(path)
    # hlines = hlines[:200]
    width = COL_WIDTH
    height = COL_HEIGHT
    im = Image.new('RGB', (width, height), color='white')
    im_draw = ImageDraw.Draw(im)
    colors = ['black']
    for y,line in enumerate(hlines):
        print '\tin:', line
        x = 0
        line = '<x>' + line # process text before HTML
        mgroups = (match.groups() for match in symbol_re.finditer(line))
        for sym, text in mgroups:
            if sym.startswith('font '):
                colors.append(sym.split('"')[1])
            elif sym == '/font':
                colors.pop()
            if not text:
                continue
            if text.startswith(' '):
                orig_len = len(text)
                text = text.lstrip(' ')
                x += orig_len - len(text)
            print '{:03d} {:10s} "{}"'.format(
                x, colors[-1], text)
            im_draw.line( (x,y, x+len(text),y), fill=colors[-1])
            x += len(text)
        print
    return im


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+')

    def handle(self, *args, **options):
        # color_iter = itertools.cycle(
        #     CMAP_COLORS + list(reversed(CMAP_COLORS)))

        for path in options['paths']:
            img = render(path)
            img.save('{}.png'.format('z'))
